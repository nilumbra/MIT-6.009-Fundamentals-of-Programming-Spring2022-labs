import re
import bz2
import gzip
import base64
import pickle
import urllib.parse

from math import acos,cos,sin,pi,atan2


def great_circle_distance(loc1, loc2):
    """
    Returns the approximate distance between (lat1, lon1) and (lat2, lon2) in
    miles, taking into account the Earth's curvature (but assuming a spherical
    earth).

    Latitude and longitudes given in degrees.  Thanks to Berthold Horn for this
    implementation.
    """
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    phi1 = lat1*pi/180.
    theta1 = lon1*pi/180.
    phi2 = lat2*pi/180.
    theta2 = lon2*pi/180.
    cospsi = sin(phi1)*sin(phi2) + cos(phi1)*cos(phi2)*cos(theta2-theta1)
    sinpsi = ((sin(theta1)*cos(phi1)*sin(phi2) - sin(theta2)*cos(phi2)*sin(phi1))**2 +\
              (cos(theta2)*cos(phi2)*sin(phi1) - cos(theta1)*cos(phi1)*sin(phi2))**2 +\
              (cos(phi1)*cos(phi2)*sin(theta2-theta1))**2)**0.5
    return atan2(sinpsi,cospsi) * 3958


def to_kml(path):
    """
    Given a path as a list of (latitude, longitude) tuples, return a string
    containing a KML[1] representation of the path, for use with the web
    viewer.

    [1] see https://en.wikipedia.org/wiki/Keyhole_Markup_Language
    """
    out = ("""<?xml version="1.0" encoding="utf-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
  <Document>
    <Placemark>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <coordinates>""")
    out += " ".join("%f,%f" % (loc[::-1]) for loc in path)
    return out + ("""</coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Start</name>
      <Point>
        <coordinates>%f,%f,0</coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>End</name>
      <Point>
        <coordinates>%f,%f,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>""" % ((path[0][::-1]) + (path[-1][::-1])))


def to_local_kml_url(path):
    """
    Given a path as a list of (latitude, longitude) tuples, return a string
    representing a URL that can be opened on the local machine to display the
    path (assuming the server is running)
    """
    b64 = base64.b64encode(to_kml(path).encode('utf-8')).decode('utf-8')
    qstring = urllib.parse.urlencode({'kml_path': 'data:application/vnd.google-earth.kml+xml;base64,%s' % b64})
    return 'http://localhost:6009/?%s' % qstring


def read_osm_data(filename):
    """
    Yield elements from the given filename, which is assumed to contain a
    series of pickled[1] Python objects, stacked end-to-end.

    This structure allows reading the large structures necessary for lab 2
    without loading the entire file into memory at once, and should be much
    faster than reading directly from a .osm file.

    Example usage:
        for element in read_osm_data('some_file'):
            print(element)

    [1] see https://docs.python.org/3/library/pickle.html
    """
    with open(filename, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def osm_to_serial_pickles(filename):
    """
    Convert the data from the given filename (assumed to represent a raw OSM
    data file, in OSM XML format[1]) to the serial pickle format used in 6.009
    lab 3.

    The filename argument is a string representing the name of a file
    containing OSM data.  The file extension is used to determine whether to
    decompress the file first or not (files ending with .gz or .bz2 are
    decompressed first).  OSM's PBF format is *not* accepted.

    Downloading raw data from [2] or [3] will usually provide files that have
    been compressed using gzip or bz2.

    It is worth mentioning that this may not work in a general sense (because
    it assumes structure that may not hold true, such as the ordering of some
    attributes), though it seems to work on data from the two sources listed
    here, and also from direct exports from [4].

    Example usage:
        osm_to_serial_pickles('resources/cambridge.osm')

    This will create files called:
        resources/cambridge.nodes
        resources/cambridge.ways
        resources/cambridge.bounds

    [1] see https://wiki.openstreetmap.org/wiki/OSM_XML
    [2] https://download.geofabrik.de/
    [3] https://download.bbbike.org/osm/
    [4] https://www.openstreetmap.org/export
    """
    node_start = re.compile(r'\s*<node.*?id="(\d+)".*?lat="(-?\d+\.?\d*)".*?lon="(-?\d+\.?\d*)".*?(/?)>')
    node_end = re.compile(r'\s*</node>')
    way_start = re.compile(r'\s*<way.*?id="(\d+)".*?>')
    way_node = re.compile(r'\s*<nd ref="(\d+)".*?/>')
    way_end = re.compile(r'\s*</way>')
    inline_tag = re.compile(r'\s*<tag.*?k="(.*?)".*?v="(.*?)".*?/>')
    bounds = re.compile(r'\s*<bounds.*?minlat="(-?\d+\.?\d*)".*?minlon="(-?\d+\.?\d*)".*?maxlat="(-?\d+\.?\d*)".*?maxlon="(-?\d+\.?\d*)".*?/>')


    # check the file extension and open the file
    filename_checker = re.compile(r'^(.*)\.((?:osm|xml)(?:.(?:gz|bz2))?)$')
    filename_match = filename_checker.match(filename)
    if filename_match:
        basename, extension = filename_match.groups()
    else:
        raise ValueError('filename should end in .gz, .bz2, .xml or .osm')

    if extension.endswith('.gz'):
        input_file = gzip.open(filename, 'rt', encoding='utf-8')
    elif extension.endswith('.bz2'):
        input_file = bz2.open(filename, 'rt', encoding='utf-8')
    else:
        input_file = open(filename, 'r', encoding='utf-8')

    bounds_file = open(f'{basename}.bounds', 'wb')
    nodes_file = open(f'{basename}.nodes', 'wb')
    ways_file = open(f'{basename}.ways', 'wb')

    try:
        current_node = None
        current_way = None
        for line in iter(input_file.readline, ''):
            if current_node is not None:
                # look for tags or ending nodes
                tag_match = inline_tag.match(line)
                if tag_match:
                    g = tag_match.groups()
                    current_node['tags'][g[0]] = g[1]
                if node_end.match(line):
                    pickle.dump(current_node, nodes_file)
                    current_node = None
            elif current_way is not None:
                # look for nodes and tags, or ending way
                tag_match = inline_tag.match(line)
                if tag_match:
                    key, value = tag_match.groups()
                    if key == 'oneway':
                        if value == 'reversible':
                            # one-way roads whose directions change with time?
                            # let's just assume the order is correct...
                            value = 'yes'
                        elif value == '-1':
                            # one-way, but in the other direction
                            value = 'yes'
                            current_way['nodes'] = current_way['nodes'][::-1]
                    current_way['tags'][key] = value
                nd_match = way_node.match(line)
                if nd_match:
                    current_way['nodes'].append(int(nd_match.group(1)))
                if way_end.match(line):
                    # try to do some conversion of speed limits so we get an
                    # integer value in the resulting object
                    for tagname in ('maxspeed', 'maxspeed:advisory'):
                        if tagname in current_way['tags']:
                            try:
                                current_way['tags']['maxspeed_mph'] = int(current_way['tags'][tagname].split()[0])
                                break
                            except:
                                pass
                    pickle.dump(current_way, ways_file)
                    current_way = None
            else:
                m1 = node_start.match(line)
                if m1:
                    g = m1.groups()
                    node = {'id': int(g[0]), 'lat': float(g[1]), 'lon': float(g[2]), 'tags': {}}
                    if g[3] != '/':
                        current_node = node
                    else:
                        pickle.dump(node, nodes_file)
                else:
                    m2 = way_start.match(line)
                    if m2:
                        g = m2.groups()
                        current_way = {'id': int(g[0]), 'nodes': [], 'tags': {}}
                    else:
                        b = bounds.match(line)
                        if b:
                            keys = ('minlat', 'minlon', 'maxlat', 'maxlon')
                            bounds_obj = dict(zip(keys, (float(i) for i in b.groups())))
                            pickle.dump(bounds_obj, bounds_file)
    except:
        raise
    finally:
        for f in (input_file, nodes_file, ways_file, bounds_file):
            f.close()


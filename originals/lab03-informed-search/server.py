import os
import sys
import json
import time
import pickle
import mimetypes

from wsgiref.handlers import read_environ
from wsgiref.simple_server import make_server

from util import to_kml, read_osm_data
from lab import find_short_path, find_fast_path, build_internal_representation

try:
    dataset = sys.argv[1]
except IndexError:
    print('please provide the name of a dataset to use', file=sys.stderr)
    print('example:', file=sys.stderr)
    print('  python3 server.py cambridge', file=sys.stderr)
    sys.exit(1)

cur_dir = os.path.realpath(os.path.dirname(__file__))
app_root = os.path.join(cur_dir, 'kml_viewer')
data_root = os.path.join(cur_dir, 'resources')

bounds_filename = os.path.join(data_root, f'{dataset}.bounds')
nodes_filename = os.path.join(data_root, f'{dataset}.nodes')
ways_filename = os.path.join(data_root, f'{dataset}.ways')

try:
    with open(bounds_filename, 'rb') as f:
        entry = pickle.load(f)
    center_point = (
        entry['minlat']*0.5 + entry['maxlat']*0.5,
        entry['minlon']*0.5 + entry['maxlon']*0.5
    )
except:
    print('could read from bounds file, using default starting position', file=sys.stderr)
    center_point = 42.3751, -71.1053


print('building internal representation...')
t = time.time()
MAP = build_internal_representation(nodes_filename, ways_filename)
print('internal representation built in %.02f seconds.' % (time.time() - t,))

with open(os.path.join(app_root, 'index.html'), 'rb') as f:
    index_contents = f.read() % center_point


def parse_post(environ):
    try:
        body_size = int(environ.get('CONTENT_LENGTH', 0))
    except:
        body_size = 0

    body = environ['wsgi.input'].read(body_size)
    return json.loads(body)


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/') or '/'

    if path == '/route':
        params = parse_post(environ)
        func = find_short_path if params.get('type', None) != 'fast' else find_fast_path
        loc1 = float(params['startLat']), float(params['startLon'])
        loc2 = float(params['endLat']), float(params['endLon'])
        route = func(MAP, loc1, loc2)
        if route is None:
            out = {'ok': False, 'error': 'No path found.'}
        else:
            out = {'ok': True, 'kml': to_kml(route)}
        body = json.dumps(out).encode('utf-8')
        type_ = 'application/json'
        status = '200 OK'
    else:
        if path == '/':
            # main page
            static_file = 'index.html'
        else:
            if path.startswith('/ui/'):
                static_file = path[4:]
            else:
                static_file = path[1:]

        test_fname = os.path.join(app_root, static_file)
        if static_file == 'index.html':
            body = index_contents
            status = '200 OK'
            type_ = 'text/html'
        elif os.path.isfile(test_fname):
            with open(test_fname, 'rb') as f:
                body = f.read()
            status = '200 OK'
            type_ = mimetypes.guess_type(test_fname)[0] or 'text/plain'
        else:
            body = b'File not found: %r' % test_fname
            status = '404 FILE NOT FOUND'
            type_ = 'text/plain'
    len_ = str(len(body))
    headers = [('Content-type', type_), ('Content-length', len_)]
    start_response(status, headers)
    return [body]


if __name__ == '__main__':
    print('starting server.  navigate to http://localhost:6009/')
    with make_server('', 6009, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()

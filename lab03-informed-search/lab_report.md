- `node` looks like:
```py
{'id': 21321186, 'lat': 42.4839446, 'lon': -71.2195117, 'tags': {}}

{'id': 21321216,
 'lat': 42.4766832,
 'lon': -71.2145382,
 'tags': {'highway': 'traffic_signals'}}

{'id': 30417351,
 'lat': 42.2030993,
 'lon': -71.1188364,
 'tags': {'highway': 'motorway_junction', 'ref': '2B'}}
```

- How many total nodes are in the database?(Hint: it may take a long time and use a large amount of memory to make a big list containing all the nodes; try looping over the result from read_osm_data instead).

There are three files containing nodes: `mit.nodes`, `midwest.nodes`,`cambridges.nodes`. So loop over these and count the total number of nodes in the database:
```py
import os
from util import read_osm_data

nodefiles = [*filter(lambda p: 'nodes' in p, os.listdir("./resources"))]
count = 0
for filepath in nodefiles:
  for node in read_osm_data((os.path.join('./resources', filepath))):
    count += 1

print(count)

$ 6838089
```


- Some of the nodes have a name associated with them (by virtue of having a 'name' entry in their 'tags' dictionary). How many of the nodes have a name?
```py
named_nodes_count = 0
for filepath in nodefiles:
  for node in read_osm_data(os.path.join('./resources', filepath)):
    if 'name' in node['tags']:
      named_nodes_count += 1
print(named_nodes_count)

$ 22257
```

- What is the ID number of the node named '77 Massachusetts Ave'?
```py
for filepath in nodefiles:
  for node in read_osm_data(os.path.join('./resources', filepath)):
    if 'name' in node['tags'] and node['tags']['name'] == '77 Massachusetts Ave':
      print(node['id'])

$ 1399811978
```

- `way` looks like:
```py
{'id': 4762630,
 'nodes': [542944370,
  30417567,
  6370679540,
  30416743,
  6370679548,
  6370679543,
  6370679551,
  30416744,
  6370682035,
  6370682028,
  6370682023,
  6370682031,
  6381501107,
  30416745,
  6381501106,
  6381501103,
  6381501094,
  6381501112,
  30417580,
  6381501100,
  6381501098,
  6381501110,
  30417581,
  6381501101,
  30417582,
  6381501108,
  6381501111,
  60822142,
  6381501097,
  30417583],
 'tags': {'bicycle': 'no',
  'destination:lanes': 'Dedham;Portsmouth New Hampshire|Dedham;Portsmouth New Hampshire|Dedham;Portsmouth New Hampshire|Dedham;Portsmouth New Hampshire;Providence Rhode Island|Providence Rhode Island',
  'foot': 'no',
  'hazmat': 'designated',
  'hgv': 'designated',
  'highway': 'motorway',
  'horse': 'no',
  'lanes': '5',
  'maxspeed': '55 mph',
  'oneway': 'yes',
  'ref': 'I 93;US 1',
  'surface': 'asphalt',
  'turn:lanes': 'none|none|none|through;slight_right|slight_right',
  'maxspeed_mph': 55}}
```

- How many total ways are in the database?
```py
wayfiles = [*filter(lambda p: 'ways' in p, os.listdir("./resources"))]
way_count = 0
for wayf in wayfiles:
  for way in read_osm_data(os.path.join('./resources', wayf)):
    way_count += 1

print(way_count)

$ 912895
```

- How many of these are one-way streets? (Hint: look at the value associated with the 'oneway' key in the 'tags' dictionary if it exists to make a decision; if that key doesn't exist, assume the road is two-way)

```py
one_way_count = 0
for wayf in wayfiles:
  for way in read_osm_data(os.path.join('./resources', wayf)):
    if 'oneway' in way['tags'] and way['tags']['oneway'] == 'yes':
      one_way_count += 1

print(one_way_count)

$ 24815
```

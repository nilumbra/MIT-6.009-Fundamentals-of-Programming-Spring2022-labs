t1 = {'value': 9, 'children': []}

t2 = {'value': 9,
      'children': [{'value': 2, 'children': []},
                   {'value': 3, 'children': []},
                   {'value': 7, 'children': []}]}

t3 = {'value': 9,
      'children': [{'value': 2, 'children': []},
                   {'value': 3,
                    'children': [{'value': 99, 'children': []},
                                 {'value': 16,
                                  'children': [{'value': 7, 'children': []}]},
                                 {'value': 42, 'children': []}]}]}

from instrument import show_recursive_structure

@show_recursive_structure
def tree_max(tree):
    best = tree['value']
    for child in tree['children']:
        child_best = tree_max(child)
        if child_best > best:
            best = child_best
    return best

print(tree_max(t3))

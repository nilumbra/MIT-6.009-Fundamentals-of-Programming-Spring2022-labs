from instrument import show_recursive_structure

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


@show_recursive_structure
def tree_max(tree):
    pass

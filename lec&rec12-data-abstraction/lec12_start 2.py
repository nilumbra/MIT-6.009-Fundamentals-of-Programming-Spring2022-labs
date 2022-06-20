graph1 = {
    13: [77, 43, 0],
    77: [-32, 28],
    0: [108],
    -32: [215],
    42: [215],
    215: [42, -32],
    28: [42],
}


def find_path(graph, start_state, goal_test):
    agenda = [(start_state,)]
    visited = {start_state}

    while len(agenda) != 0:
        path = agenda.pop(0)
        terminal_state = path[-1]

        if goal_test(terminal_state):
            return list(path)

        children = []
        for key in graph:
            if key == terminal_state:
                children = graph[key]

        for child in children:
            if child not in visited:
                agenda.append(path + (child,))
                visited.add(child)

    return None


print(find_path(graph1, 13, lambda x: x == -32))

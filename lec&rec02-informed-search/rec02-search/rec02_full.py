# successors: function state -> list of neighboring states
def search(successors, start, goal_test, dfs=False):
    if goal_test(start):
        return (start,)

    agenda = [(start,)]
    visited = {start}

    while len(agenda) != 0:
        current_path = agenda.pop(-1 if dfs else 0)
        terminal_vertex = current_path[-1]

        for child in successors(terminal_vertex):
            new_path = current_path + (child,)
            if goal_test(child):
                return new_path
            elif child not in visited:
                agenda.append(new_path)
                visited.add(child)

    return None

with open('words.txt') as f:
    all_words = {i.strip() for i in f}

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
def word_successors(state):
    possible = {
        state[:ix] + l + state[ix+1:]
        for ix in range(len(state))
        for l in LETTERS
    }
    return possible & all_words

print(search(word_successors, 'fool', lambda x: x == 'sage', dfs=False))

def format_sudoku(board):
    """
    Format a sudoku board to be printed to the screen
    """
    _divider = '+'+''.join('-+' if i%3==2 else '-' for i in range(9))
    lines = []
    for i in range(9):
        if i % 3 == 0:
            lines.append(_divider)
        line = '|'
        for j in range(9):
            line += ' ' if board[i][j] == 0 else str(board[i][j])
            if j % 3 == 2:
                line += '|'
        lines.append(line)
    lines.append(_divider)
    return '\n'.join(lines)


def values_in_row(board, r):
    """
    Return a set containing all of the values in a given row.
    """
    return board[r]


def values_in_column(board, c):
    """
    Return a list containing all of the values in a given column.
    """
    return [board[r][c] for r in range(len(board))]


def values_in_subgrid(board, sr, sc):
    """
    Return a list containing all of the values in a given subgrid.
    """
    return [board[r][c]
            for r in range(sr*3, (sr+1)*3)
            for c in range(sc*3, (sc+1)*3)]


def solve_sudoku(board):
    """
    Given a sudoku board (as a list-of-lists of numbers, where 0 represents an
    empty square), return a solved version of the puzzle.

    If the puzzle cannot be solved, return None.
    """
    pass


grid1 = [[5,1,7,6,0,0,0,3,4],
         [2,8,9,0,0,4,0,0,0],
         [3,4,6,2,0,5,0,9,0],
         [6,0,2,0,0,0,0,1,0],
         [0,3,8,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

grid2 = [[5,1,7,6,0,0,0,3,4],
         [0,8,9,0,0,4,0,0,0],
         [3,0,6,2,0,5,0,9,0],
         [6,0,0,0,0,0,0,1,0],
         [0,3,0,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

grid3 = [[0,0,1,0,0,9,0,0,3],
         [0,8,0,0,2,0,0,9,0],
         [9,0,0,1,0,0,8,0,0],
         [1,0,0,5,0,0,4,0,0],
         [0,7,0,0,3,0,0,5,0],
         [0,0,6,0,0,4,0,0,7],
         [0,0,8,0,0,5,0,0,6],
         [0,3,0,0,7,0,0,4,0],
         [2,0,0,3,0,0,9,0,0]]

grid4 = [[1,0,0,0,6,0,0,0,9],
         [0,9,0,1,0,5,0,8,0],
         [0,0,7,0,8,0,3,0,0],
         [0,8,0,0,0,0,0,6,0],
         [4,0,5,0,0,0,8,0,3],
         [0,1,0,0,0,0,0,4,0],
         [0,0,9,0,3,0,1,0,0],
         [0,6,0,2,0,9,0,3,0],
         [2,0,0,0,7,0,0,0,5]]

grid5 = [[5,0,1,8,0,3,7,0,2],  # http://www.extremesudoku.info/sudoku.html
         [0,0,0,0,0,0,0,0,0],
         [7,0,0,2,0,5,0,0,8],
         [6,0,2,0,0,0,4,0,7],
         [0,0,0,0,5,0,0,0,0],
         [1,0,7,0,0,0,9,0,5],
         [8,0,0,9,0,2,0,0,3],
         [0,0,0,0,0,0,0,0,0],
         [2,0,9,5,0,7,6,0,1]]

grid6 = [[0,8,0,0,0,0,0,9,0],  # https://sudoku.com/expert/
         [0,1,0,0,8,6,3,0,2],
         [0,0,0,3,1,0,0,0,0],
         [0,0,4,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,5],
         [0,0,0,2,6,1,0,0,4],
         [0,0,0,5,4,0,0,0,6],
         [3,0,9,0,0,0,8,0,0],
         [2,0,0,0,0,0,0,0,0]]


import time
for grid in [grid1, grid2, grid3, grid4, grid5, grid6]:
    print(format_sudoku(grid))
    t = time.time()
    res = solve_sudoku(grid)
    assert res is not None
    elapsed = time.time() - t
    print(format_sudoku(res))
    print(elapsed, 'seconds')
    print()

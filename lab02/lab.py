# 6.009 Lab 2: Snekoban

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

##### utility functions #####
def isMovable(game, direction):
    y, x = game["player"]
    dy, dx = direction
    r, c = game["size"][0], game["size"][1]

    # Check if the player is moving into a wall cell
    if (0 < x+dx < c - 1 and 0 < y+dy < r - 1 and (y+dy, x+dx) not in game["walls"]):
        
        # if there are two consecutive computers in the direction of move, or there is a computer, then a wall in the direction of move, return false
        if (y+dy, x+dx,) in game["computers"] and ((y + dy + dy, x + dx + dx,) in game["computers"] or game["walls"] or (y + dy + dy >= r - 1 or y + dy + dy <= 0 or x + dx + dx >= c - 1 or x + dx + dx <= 0)):
            # print("Computers can't be push because there's a computer or a wall in the direction")
            return False
        else: 
            return True
    else: # Out of bounds
        return False

def update_pos(player, direction):
    """
    Given player and direction in tuples.
    Return the pair-wise addition of them
    """
    # print(player, direction, tuple(map(lambda i, j: i+j, player, direction)))
    return tuple(map(lambda i, j: i+j, player, direction))

def move(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game after applying either of the four directions as following
    up : (-1, 0) / down: (+1, 0) / left: (0, -1), / right: (0, +1)
    """

    ### SPECS OF IMPLEMENTATION:
    #1: FREE MOVE IGNORING WALLS BUT TAKE INTO ACCOUNT BOUNDS
    #2: MOVING AGAINST WALLS DOES NOT CHANGE THE GAME STATE
    #3: PUSHING A COMPUTER WHEN THE NEXT CELL IN THE DIRECTION IS OCCUPIED BY WALL OR COMPUTER DOES NOT CHANGE THE GAME STATE
    #4: PUSHING A COMPUTER WHEN THE NEXT CELL IN THE DIRECTION IS EMPTY MOVES BOTH THE PLAYTHE COMPUTER IN THAT DIRECTION BY ONE UNIT
    size, player, targets, walls, computers = game["size"], game["player"], game["targets"], game["walls"], set(game["computers"])

    if(isMovable(game, direction)):
        new_player = update_pos(player, direction)
        if new_player in computers: # Movable computer
            computers.remove(new_player)
            computers.add(update_pos(new_player, direction))

        return {
            "size": size, 
            "player": new_player,
            "targets": targets,
            "walls": game["walls"],
            "computers": computers,
        }
    else:
        return game 
    

def new_game(level_description):
    global s2d
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """

    player_pos = None
    targets = set()
    computers = set()
    walls = set()
    
    for (rid, orow) in enumerate(level_description):
        for (cid, cell) in enumerate(orow):
            for el in cell:
                if el == "player":
                    player_pos = (rid, cid)
                elif el == "target":
                    targets.add((rid, cid))
                else:
                    if (el == "computer"): computers.add((rid, cid))
                    if (el == "walls"): walls.add((rid, cid))

    return {
            "size": (len(level_description), (len(level_description[0]))), # (, rowNum, colNum) 
            "player": player_pos, 
            "targets": targets,
            "computers": computers,
            "walls": walls,
        }



def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    return game["computers"] == game["targets"]

def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    global direction_vector
    return move(game, direction_vector[direction])



def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """

    canonical = [[[] for j in range(game["size"][1])] for i in range(game["size"][0])]
    for (i, j) in game["targets"]:
        canonical[i][j].append("target")

    for i, j in game["walls"]:
        canonical[i][j].append("wall")

    # top and bottom
    for j in range(game["size"][1]):
        canonical[0][j].append("wall") 
        canonical[game["size"][0] - 1][j].append("wall") 

    # left and right
    for i in range(1, game["size"][0] - 1): 
        canonical[i][0].append("wall")
        canonical[i][game["size"][1] - 1].append("wall")

    for i, j in game["computers"]:
        canonical[i][j].append("computer")

    px, py = game["player"]
    canonical[px][py].append("player")

    return canonical


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    raise NotImplementedError


if __name__ == "__main__":
    pass

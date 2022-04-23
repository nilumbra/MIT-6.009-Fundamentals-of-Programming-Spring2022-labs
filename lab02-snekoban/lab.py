# 6.009 Lab 2: Snekoban

import json
import typing
import copy
import heapq
from collections import deque
import functools
# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

reverse_direction_vector = {
    (-1, 0): "up",
    (+1, 0): "down",
    (0, -1): "left",
    (0, +1): "right"
}

##### utility functions #####
def print_pretty(canonical):
    for row in canonical:
        print(row)

def isMovable(game, direction):
    y, x = game["player"]
    dy, dx = direction
    r, c = game["size"][0], game["size"][1]

    # print_pretty(dump_game(game))
    # Check if the player is moving into a wall cell
    if (0 < x+dx < c - 1 and 0 < y+dy < r - 1 and (y+dy, x+dx) not in game["walls"]):
        # if there are two consecutive computers in the direction of move, or there is a computer, then a wall in the direction of move, return false
        if (y+dy, x+dx,) in game["computers"] and ((y + dy + dy, x + dx + dx,) in game["computers"] or (y + dy + dy, x + dx + dx,) in game["walls"] or (y + dy + dy >= r - 1 or y + dy + dy <= 0 or x + dx + dx >= c - 1 or x + dx + dx <= 0)):
            # print("Computers can't be push because there's a computer or a wall in the direction")
            return False
        else: 
            # print("Movable")
            return True
    else: # Out of bounds
        # print("Unmovable because it is a move that will result in the player getting out of bounds.")
        return False

def update_pos(player, direction):
    """
    Given player and direction in tuples.
    Return the pair-wise addition of them
    """
    # print(player, direction, tuple(map(lambda i, j: i+j, player, direction)))
    return tuple(map(lambda i, j: i+j, player, direction))

def move(game, direction):
    global reverse_direction_vector
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
    player, computers = game["player"], set(game["computers"])

    if(isMovable(game, direction)):
        new_player = update_pos(player, direction)
        print(f'Player at {player} moves {reverse_direction_vector[direction]} to {new_player}')
        if new_player in computers: # Movable computer
            print (f'Player at {player} pushed computer at {new_player} {reverse_direction_vector[direction]} to {update_pos(new_player, direction)}')
            computers.remove(new_player)
            computers.add(update_pos(new_player, direction))



        new_game = {
            "size": game["size"], 
            "player": new_player,
            "targets": game["targets"],
            "walls": game["walls"],
            "computers": computers,
            "corners": game["corners"]
        }
        
        # print(new_game)

        return new_game
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
                    if (el == "wall"): walls.add((rid, cid))

    
    new_game = {
            "size": (len(level_description), (len(level_description[0]))), # (, rowNum, colNum) 
            "player": player_pos, 
            "targets": targets,
            "computers": computers,
            "walls": walls,
        }

    augment_corners(new_game)
    return new_game


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    # print (f'computers:{game["computers"]}', f'targets:{game["targets"]}')
    return len(game["computers"]) * len(game["targets"]) != 0 and len(game["computers"]) == len(game["targets"]) and game["computers"] == game["targets"]

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

    ### Assume that the four sides are walled
    # # top and bottom
    # for j in range(game["size"][1]):
    #     canonical[0][j].append("wall") 
    #     canonical[game["size"][0] - 1][j].append("wall") 

    # # left and right
    # for i in range(1, game["size"][0] - 1): 
    #     canonical[i][0].append("wall")
    #     canonical[i][game["size"][1] - 1].append("wall")

    for i, j in game["computers"]:
        canonical[i][j].append("computer")

    px, py = game["player"]
    canonical[px][py].append("player")

    return canonical


###### Solver Utilities ######
def isRecoverable(game, computer, direction): 
    """
    Given a <game> representing current state of Snekoban, a <computer> tuple representing the position of the computer to test for a reverse move, and <direction> representing the direction of that reverse move.
    Determine if that reverse move is valid according to the rules of Snekoban.
    """
    inferred_player = update_pos(computer, direction+direction)

    return inferred_player not in (game["walls"] | game["computers"])
    
## TESTED: OK
def augment_corners(game):
    global direction_vector
    """
    Given a game object, augment the object with a game["corners"] property
    """
    CORNER_CONF = ((direction_vector["up"], direction_vector["left"]),
                    (direction_vector["up"], direction_vector["left"]),
                    (direction_vector["down"], direction_vector["left"]),
                    (direction_vector["down"], direction_vector["right"]),
                    )

    corners = set()
    for i in range(game["size"][0]):
        for j in range(game["size"][1]):
            for cf in CORNER_CONF:
                if (i, j) not in game["walls"] and update_pos((i, j), cf[0]) in game["walls"] and update_pos((i, j), cf[1]) in game["walls"]:
                    corners.add((i, j))

    game["corners"] = corners

# TEST: OK (Maybe?)
def isWallOccupiable(game, computer, direction):
    """
    Given a computer pos. Determine, in accordance with Ob.1.1, whether the wall is occupiable.
    """
    global reverse_direction_vector
    global direction_vector

    y,x = computer
    # if downblock and upblock is not None in the end 
    if reverse_direction_vector[direction] in {"left", "right"}:
        downblock, upblock = (y, x), (y, x)
        numTargets = 0
        numComputersAlongWall = 0

        # Scan below
        while downblock[0] < game["size"][0] - 1:
            print("down", downblock)
            # A move into wall is good if it is not indeed an closed wall
            if update_pos(downblock, direction_vector["left"]) not in game["walls"] and update_pos(downblock, direction_vector["right"]) not in game["walls"]:
                return True

            # In the spirit of Ob.1.2, we count computer cells along the wall
            if downblock in game["computers"]:
                numComputersAlongWall += 1

            # In the spirit of Ob.1.2, we count target cells along the wall
            if downblock in game["targets"]:
                numTargets += 1

            # Reach a corner. Hence confirmed bottom is closed
            if downblock in game["corners"]:
                break

            downblock = update_pos(downblock, direction_vector["down"])


        # Scan above
        while 0 < upblock[0]:
            print("up", upblock)
            # A move into wall is good if it is not indeed an closed wall
            if update_pos(upblock, direction_vector["left"]) not in game["walls"] and update_pos(upblock, direction_vector["right"]) not in game["walls"]:
                return True

            # In the spirit of Ob.1.2, we count target cells along the wall
            if upblock in game["targets"]:
                numTargets += 1

            # In the spirit of Ob.1.2, we count computer cells along the wall
            if upblock in game["computers"]:
                numComputersAlongWall += 1

            # Reach a corner. Hence confirmed bottom is closed
            if upblock in game["corners"]:
                break
            
            upblock = update_pos(upblock, direction_vector["up"])
        print("#Comp", numComputersAlongWall, "#Targ", numTargets)

        # Don't forget to count the computer currently being pushed!!
        return numTargets > numComputersAlongWall 

    # if leftblock and rightblock is not None in the end 
    if reverse_direction_vector[direction] in {"up", "down"}:
        leftblock, rightblock = (y, x), (y, x)
        numTargets = 0
        numComputersAlongWall = 0

        # Scan left
        while 0 < leftblock[1]:
            print("left", leftblock)
            # A move onto wall is good if the wall is not indeed a closed one
            if update_pos(leftblock, direction_vector["up"]) not in game["walls"] and update_pos(leftblock, direction_vector["down"]) not in game["walls"]:
                return True

            # In the spirit of Ob.1.2, we count computer cells along the wall
            if leftblock in game["computers"]:
                numComputersAlongWall += 1

            # In the spirit of Ob.1.2, we count target cells along the wall
            if leftblock in game["targets"]:
                numTargets += 1

            # Reach a corner. Hence confirmed bottom is closed
            if leftblock in game["corners"]:
                break            

            leftblock = update_pos(leftblock, direction_vector["left"])

        # Scan above
        while rightblock[0] <  game["size"][1] - 1:
            print("right", rightblock)
            # A move into wall is good if it is not indeed an closed wall
            if update_pos(rightblock, direction_vector["up"]) not in game["walls"] and update_pos(rightblock, direction_vector["down"]) not in game["walls"]:
                return True

            # In the spirit of Ob.1.2, we count target cells along the wall
            if rightblock in game["targets"]:
                numTargets += 1

            # In the spirit of Ob.1.2, we count computer cells along the wall
            if rightblock in game["computers"]:
                numComputersAlongWall += 1

            # Reach a corner. Hence confirmed bottom is closed
            if rightblock in game["corners"]:
                break
            
            rightblock = update_pos(rightblock, direction_vector["right"])
        print("#Comp", numComputersAlongWall, "#Targ", numTargets)
        return numTargets > numComputersAlongWall

# Deprecated
def isReachable(game, goto):
    """
    Determine whether there is a path between game["player"] and goto.
    This function will first read off from the game["reachable"], which is an augmented property appended by this function as well. The property stores a dictionary where the key is a tuple composed as (player_pos, ...computer_pos, goto) and a boolean value indicating whether it is possible to move from <player_pos> to <goto> under the configuration its tuple key represents.
    If no such key in game["reachable"], then do a breath first search. If the path length >= 5 or there is no path available for the configuration, store them in game["reachable"]
    """
    # curr_conf = tuple([game["player"]] + [*tuple(sorted(computers))] + [goto])
    # if curr_conf in game["reachable"]:
    #     return game[curr_conf]

    # Do breadth first search for a path between
    path = findShortestPath(game, game["player"], goto)

    if path is not None:
        return True
    else:

        return False

## TESTED: OK
def findShortestPath(game, start, goto):
    global direction_vector
    """
    Given a game state, find the shortest path between <start> and <goto>, return the shortest path as a list with list[0] == start and list[-1] == goto. Return None if no path found.
    """
    if start in game["walls"] or start in game["computers"]: return None

    seen = {start}
    frontier = []
    parent = {start: None}
    h = lambda curr, step: step + abs(curr[0] - goto[0]) + abs(curr[1] - goto[1])

    heapq.heappush(frontier, (0, h(start, 0), start)) # (step, cost, (y, x))


    while frontier:
        step, cost, (y, x) = heaq.heappop(frontier)
        for dy, dx in direction_vector.values():
            neighbor = (y + dy, x + dx)
            if neighbor in seen or neighbor in game["walls"] or neighbor in game["computers"]:
                continue
            else:
                parent[neighbor] = (y, x)
                seen.add(neighbor)
                heapq.heappush(frontier, (step+1, h(neighbor, step+1), neighbor))

            if neighbor == goto: # If found a path, break out of while loop
                break

    if goto not in parent:
        return None
    else:
        shortestPath = []
        ptr = goto
        while parent[ptr]:
            shortestPath.append(ptr)
            ptr = parent[ptr]
        shortestPath.append(ptr)
        return shortestPath[::-1]

## TESTED: OK
def readable_path(path):
    global reverse_direction_vector
    get_direction = lambda fromm, to: (to[0] - fromm[0], to[1] - fromm[1])

    if path is not None: 
        for i in range(len(path) - 1):
            print("Moving from {0} {1} to {2}\n".format(path[i], reverse_direction_vector[(get_direction(path[i], path[i+1]))],path[i+1]))
    else:
        print("No path found")
    
# TEST: OK (Maybe?)
def canMove(game, computer, direction):
    """
    Given a game state, determine whether moving <computer> in <direction> is reasonable.
    Return True for a reasonable move, otherwise return False

    By observing the game mechanism, we know certain types of move should never be made considering the current state of the game, because these futile moves leads game to a dead end. 

    Observation 1: 
    Let the number of targets sitting next to a section of closed wall be T, and the number of computers next to closed wall be C. Invariant C <= T must hold in order to win the game. Since we cannot push computers next to a section of closed wall in any other direction that it extends itself. 
    1.1 If the corner is not a target, never push a computer into the corner.
    1.2 In addition to ob.1, we further observe that number of computers sitting along a closed wall <A> should not exceed the number of target cell along that same wall. 
    
    Observation 2:
    A computer move is possible 
     the computer-forward-player-behind spacial arragement  

    This function determines whether moving a computer in a certain direction based on the current state of the game is an acceptable move by implementing above-mentioned observation.
    """

    # By observation 1, we should never push a computer up to a closed wall along which there are no target cells.
    dy, dx = direction
    player = tuple(game["player"])
    afterMove = update_pos(computer, direction)

    # Ob. 1.1
    if afterMove in game["corners"] and afterMove not in game["targets"]:
        print("Push into a non-target corner is not valid!!")
        return False

    # Basic mechanics: pushing into a wall cell or computer is not allowed
    if afterMove in game["walls"] | game["computers"]: 
        print("Push into a wall cell or computer cell is not valid!!")
        return False

    # is wall in direction and the wall is not occupiable?
    if update_pos(computer, (dy*2, dx*2)) in game["walls"] and not isWallOccupiable(game, afterMove, direction): 
        print("Unoccupiable wall. This move leads to a dead end.")
        return False

    path = findShortestPath(game, game['player'], update_pos(computer, (-dy, -dx)))

    readable_path(path)

    if path is not None:
        return True
    else:
        return False

def get_moves(parents, last_state):
    global reverse_direction_vector
    """
    ##DEPRECATED COMMENT##

    Given a game and a trace of computers' moves, reconstruct the player's move that makes the entire trace of computers' move possible.
    Return the reconstructed player's move trace.

    Implmentation note: 
    Make a workable version using breadth-first search first. 
    Then try A* to optimize speed.
    """    
    get_direction = lambda to, fromm: (to[0] - fromm[0], to[1] - fromm[1])
    moves = [] 

    while parents[last_state]:
        prev_state = parents[last_state]
        move = get_direction(last_state[0], prev_state[0])
        if move in reverse_direction_vector:
            moves.append(reverse_direction_vector[move])

        last_state = prev_state
        print(last_state, prev_state)

    return list(reversed(moves))

def heuristic_maker(targets):
    # Return a heuristic function that calculates the cost as a sum of hamilton distance of closest 
    def h(current_state):
        current_state, targets = sorted(current_state), sorted(targets)
        if len(current_state) != len(targets): 
            raise ValueError("Unmatched length: the number of computers do not match with the number of targets!!")    
        total_hamilton = 0
        for c, t in zip(sorted(current_state), sorted(targets)):
            total_hamilton += abs(c[0] - t[0]) + abs(c[1] - t[1])
        return total_hamilton
    return h


def get_next_state(game, direction):
    return update_pos(game["player"], direction)

##############################
class Trace:
    def __init__(self):
        global direction_vector
        ## moving trace of computer from p1 to p2, e.g.
        #  ((1,1), (1, 2)) means moving computer at (1, 1) to (1, 2)
        #
        # next: reference of another trace object representing the move immediately after this one
        self.records = []
        
    def append_record(self, record):
        self.records.append(record)

    def __repr__(self):
        return [str(record) for record in self.records]

class Record:
    global reverse_direction_vector
    def __init__(self, move=None, step=0, nxt=None, prev=None, playermove=[]):
        """
        self.move: ((int,int), (int, int))
        """
        self.move = move
        self.playermove = playermove
        self.step = step
        self.next = nxt
        self.prev = prev

    @property
    def movetext(self): 
        return reverse_direction_vector[tuple((j - i for i,j in zip(*self.move)))]

    @property
    def playermove(self): 
        return [reverse_direction_vector[tuple((j - i for i,j in zip(*playermove)))] for playermove in self.playermove]

    def __repr__(self):
        return "Moving computer at {0} {1} to {2}\n".format(self.move[0], self.movetext, self.move[1])

def solve_puzzle(game):
    global direction_vector
    global reverse_direction_vector
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    # level = copy.deepcopy(game)
    # target_state = tuple(game["targets"])
    # start_state = tuple(game["computers"])
    # step = 0
    # trace = Trace()

    # augment_corners(game) # Add 'corners' property to the game


    # # isStart = isBackToStart(start_state)
    # h = heuristic_maker(curr_state)
    
    # seenState = set()

    # def DFS_forward(game, step, trace):
    #     global reverse_direction_vector
    #     """
    #     Find the series of moves that take the <game> from <curr_state> to <target_state> in minimum number of steps.
    #     Record the state transition relation by modifying <parent> dictionary.
    #     """

    #     best_step, best_record, best_move, best_movetext = float('inf'), None, None, ""
    #     curr_record = Record()
        
    #     seenState.add(curr_state)
    #     for c in game["computers"]:
    #         for direction in {(0, -1), (-1, 0), (0, +1), (+1, 0)}: 
    #             changedComputer = update_pos(c, direction)
    #             changedState = tuple(set(curr_state) - { c } | {changedComputer}) 


    #     ## Hook the best path to the higher state in the search tree
    #     if best_trace:
    #         trace.movetext = best_movetext
    #         trace.move = best_move        
    #         trace.next = best_trace
    #         best_trace.prev = trace

    #     # If no valid path found down the tree, return best_trace as None
    #     return (best_step, curr_trace) if best_step != float('inf') else (float('inf'), None)

    def BFS(game):
        """
        Each valid (game["player",) + game["computers"] tuple represents a game state. Visualizing them as nodes in a graph, the edges are all possible transitions(moves) that take one state into another. Once the algorithm reaches the target state, it should return the trace from the starting state to end state.
        """
        seen_states = set()
        frontier = deque()

        start_state = (game["player"], ) + tuple(game["computers"])
        parents = {start_state: None}
        print('Start state: {start_state}')

        seen_states.add(start_state)
        frontier.append(start_state)
        while frontier:
            curr_state = frontier.popleft()
            # Mock the current game state
            game["player"], game["computers"] = curr_state[0], curr_state[1:]
            print(f'Player at {game["player"]}. Computers at {game["computers"]}')
            for direction in reverse_direction_vector:
                stepped_game = move(game, direction)
                print(f'Changing state... Now player at {game["player"]}, computers at: {game["computers"]}')
                next_state = (stepped_game["player"],) + tuple(stepped_game["computers"]) 
                if set(next_state[1:]) == game["targets"]:
                    print(f'Reached target state: {game["targets"]}. Computers: {set(next_state[1:])}')
                    parents[next_state] = curr_state
                    return (next_state, parents) # Traversing the parents tree from next_state will form a path to start_state

                if next_state not in seen_states:
                    seen_states.add(next_state)
                    frontier.append(next_state)
                    parents[next_state] = curr_state

        # print(parents)
        return None

    solution_digest = BFS(game)
    if solution_digest:
        last_state, parents = solution_digest
        moves = get_moves(parents, last_state)
        return moves
    else:
        return None

def solve_puzzle_backwards(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    def isBackToStart(start_state):
        def f(current_state, computer, direction):
            return set(current_state) - { computer } | { update_pos(computer, direction) } == set(start_state)
        return f

    def isMoveRecoverable(game):
        def f(computer, direction):
            return isRecoverable(game, computer, direction)
        return f
    def isMovableInner(game):
        def f(direction):
            return isMovable(game, direction)
        return f

    level = copy.deepcopy(game)
    target_state = tuple(game["targets"])
    start_state = tuple(game["computers"])
    step = 0
    trace = Trace()


    # isStart = isBackToStart(start_state)
    h = heuristic_maker(curr_state)
    
    seenState = set()

    def DFS_backwards(curr_state, step, trace):
        global reverse_direction_vector
        print(curr_state)
        """
        Find the series of moves that take the <game> from <curr_state> to <start_state> in minimum number of steps.
        Record the state transition relation by modifying <parent> dictionary.
        """
        best_step, best_trace, best_move, best_movetext = float('inf'), None, None, ""
        curr_trace = Trace()
        trace.prev = curr_trace
        seenState.add(curr_state)
        for c in curr_state:
            for direction in {(0, -1), (-1, 0), (0, +1), (+1, 0)}: 
                changedComputer = update_pos(c, direction)
                changedState = tuple(set(curr_state) - { c } | {changedComputer})
                if changedState not in seenState and canMoveBack(c, direction):
                    if isStart(curr_state, c, direction):
                    # BASE CASE: All computers made their way back to their starting positions, hence a path is found
                        curr_trace.move = (changedComputer, c) # starting position -> c
                        curr_trace.movetext = reverse_direction_vector[direction]
                        curr_trace.next = trace
                        return step + 1
                    else:
                    ### Move <c> in the <direction> does not bring the <curr_state> back to <start_state>. We explore further.
                        __step, __trace = DFS(changedState, step + 1, curr_trace)

                        if  __trace and __step < best_step:
                            best_step = __step
                            best_trace = __trace
                            best_move = (changedComputer, c)
                            best_movetext = reverse_direction_vector[direction]
                        print(reverse_direction_vector[direction])
                else:
                    # <c> can't move in the <direction>, try another direction
                    continue

            # Try moving other computers 


        ## Hook the best path to the higher state in the search tree
        if best_trace:
            curr_trace.movetext = best_movetext
            curr_trace.move = best_move        
            best_trace.next = curr_trace
            curr_trace.prev = best_trace

        # If no valid path found down the tree, return best_trace as None
        return (best_step, curr_trace) if best_step != float('inf') else (float('inf'), None)

    return DFS_backwards(curr_state, 0, trace)  

if __name__ == "__main__":
    pass

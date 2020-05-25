#a1.py

from search import *
import time

# python passing info
# **modifying** a passed object will maintain pass by reference
# **reassigning** a passed object will break shared reference, act as pass by value

#------------ Question 1 ------------#

# shuffle the 8-puzzle by starting with the goal
# and making a random number of random legal moves
def shufflePuzzle(puzzle):
    #goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    #move a random number of times
    numMoves = random.randint(151, 200)
    for x in range(numMoves):
        actions = puzzle.actions(puzzle.initial)
        randChoice = random.randint(0, len(actions)-1)
        newState = puzzle.result(puzzle.initial, actions[randChoice])
        #puzzle = EightPuzzle(newState, goal)
        puzzle = EightPuzzle(newState)
    
    return puzzle

def make_rand_8puzzle():
    #create and shuffle 8-puzzle
    state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = EightPuzzle(state)
    puzzle = shufflePuzzle(puzzle)
    state = puzzle.initial
    #verify solvability of createRandom8Tuple
    while not puzzle.check_solvability(state):
        print("Generated 8-puzzle not solvable, trying again...")
        
        #puzzle = EightPuzzle(state, goal)
        puzzle = EightPuzzle(state)

        puzzle = shufflePuzzle(puzzle)
        state = puzzle.initial
        
    print("Found solvable 8-puzzle")
    return puzzle

def display(state):
    strRow = ""
    for i in range(9):
        #replace 0 with *
        if state[i] == 0:
            strRow += "*"
        else:
            strRow += str(state[i])

        #check for last char in row & print
        if (i + 1) % 3 == 0:
            print(strRow)
            strRow = ""
        else:
            strRow += " "


#------------ Question 2 ------------#

# ~~Heuristics~~ #
# Misplaced Tile Heuristic
# need to redefine to take max
# taken from method EightPuzzle.h()
def MisplacedTileHeuristic(node, goal = (1,2,3,4,5,6,7,8,0)):
    return sum(s != g for (s, g) in zip(node.state, goal))

# Manhattan Heuristic
# TODO verify if empty tile should be included in calculation 
def ManhattanHeuristic(node):
    #pre-computed Manhattan estimation - retrieved from notes on Chapter 3
    listEstimation = [
        (0,1,2,1,2,3,2,3,4),
        (1,0,1,2,1,2,3,2,3),
        (2,1,0,3,2,1,4,3,2),
        (1,2,3,0,1,2,1,2,3),
        (2,1,2,1,0,1,2,1,2),
        (3,2,1,2,1,0,3,2,1),
        (2,3,4,1,2,3,0,1,2),
        (3,2,3,2,1,2,1,0,1),
        (4,3,2,3,2,1,2,1,0)
    ]
    
    #track total cost of node
    cost = 0
    #track current position of nodeTile in grid
    tilePosition = 0
    # nodeTile = the value of the tile in grid (0-8)
    for nodeTile in node.state:
        # tile #0 goes in the last position,
        # all other tiles must be moved left 1 index
        if nodeTile != 0:
            tileHomePosition = nodeTile - 1
        else: 
            tileHomePosition = 8

        cost += listEstimation[tileHomePosition][tilePosition]
        tilePosition += 1
        
    return cost

# max of Misplaced Tile and Manhattan Heuristic
def maxMisplacedManhattan(node):
    return max(ManhattanHeuristic(node), MisplacedTileHeuristic(node))

# ~~A* Function Calls~~ #

# taken from search.py, modified to record frontier pops
# combined astar_search() and best_first_graph_search() functions
def astarSearch(problem, h=None):

    countFrontierPop = 0
    h = memoize(h or problem.h, 'h')
    f = lambda n: n.path_cost + h(n)
    
    f = memoize(f, 'f')

    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        countFrontierPop += 1
        if problem.goal_test(node.state):
            # if display:
            #     print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return (node, countFrontierPop)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


#seach using Misplaced Tile heuristic
def searchAStarMisplacedTile(state):
    print("Solving with Misplaced Tile heuristic...")
    puzzle = EightPuzzle(state)
    start_time = time.time()
    # TODO modify A* algorithm to display total number of tiles moved and total number of tiles remaining in frontier
    # [0] = node, [1] = # of nodes popped from frontier
    tupleSolution = astarSearch(puzzle)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)


#search using Manhattan heuristic
def searchAStarManhattan(state):
    print("Solving with Manhattan heuristic...")
    puzzle = EightPuzzle(state)
    start_time = time.time()
    tupleSolution = astarSearch(puzzle, ManhattanHeuristic)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)


#search using max of Misplaced Tile and Manhattan
def searchAStarMax(state):
    print("Solving with max(Misplaced, Manhattan) heuristic...")
    puzzle = EightPuzzle(state)
    start_time = time.time()
    tupleSolution = astarSearch(puzzle, maxMisplacedManhattan)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)


def printHeuristicResults(tupleSolution, elapsed_time):
    print("--> Elapsed time: " + str(round(elapsed_time, 2)) + " seconds")
    print("--> Solution length: " + str(len(tupleSolution[0].solution())) + " tiles moved")
    print("--> Nodes removed from frontier: " + str(tupleSolution[1]))
    print()






#------------ Global Space ------------#
puzzle = make_rand_8puzzle()
print("Solving following 8-puzzle with multiple heuristics...")
display(puzzle.initial)

#state = (4,7,2,0,6,5,3,8,1)

# search using Misplaced Tile heuristic
searchAStarMisplacedTile(puzzle.initial)

#search using Mahattan heuristic
searchAStarManhattan(puzzle.initial)

#search using max of Manhattan and Misplaced Tile
searchAStarMax(puzzle.initial)
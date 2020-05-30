#a1.py

from search import *
import time

# python passing info
# **modifying** a passed object will maintain pass by reference
# **reassigning** a passed object will break shared reference, act as pass by value

#---------------------------------------------------- Question 1 ----------------------------------------------------#

# shuffle a Problem object by starting with the goal
# and making a random number of random legal moves
def shufflePuzzle(puzzle):
    #move a random number of times
    numMoves = random.randint(151, 200)
    for x in range(numMoves):
        actions = puzzle.actions(puzzle.initial)
        randChoice = random.randint(0, len(actions)-1)
        newState = puzzle.result(puzzle.initial, actions[randChoice])
        puzzle.initial = newState
    
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
        state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        puzzle.initial = state
        puzzle = shufflePuzzle(puzzle)
        state = puzzle.initial

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

#---------------------------------------------------- Question 2 ----------------------------------------------------#

# ~~EightPuzzle Heuristics~~ #
# Misplaced Tile Heuristic - works for Eight and Duck Puzzle
# redefining from search.py to make it admissible (not include 0)
def MisplacedTileHeuristic(node, goal = (1,2,3,4,5,6,7,8,0)):
    #total number of tiles out of position
    count = 0

    for itrTile in range(9):
        if node.state[itrTile] != goal[itrTile]: 
            if node.state[itrTile] != 0:
                count += 1
    return count

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
        # tile home position is 1 index left of tile value
        # 0 tile shouldn't be counted in heuristic
        if nodeTile != 0:
            tileHomePosition = nodeTile - 1
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
    print("\nSolving with Misplaced Tile heuristic...")
    puzzle = EightPuzzle(state)
    start_time = time.time()
    # tupleSolution: [0] = node, [1] = # of nodes popped from frontier
    tupleSolution = astarSearch(puzzle, MisplacedTileHeuristic)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)

#search using Manhattan heuristic
def searchAStarManhattan(state):
    print("\nSolving with Manhattan heuristic...")
    puzzle = EightPuzzle(state)
    start_time = time.time()
    tupleSolution = astarSearch(puzzle, ManhattanHeuristic)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)

#search using max of Misplaced Tile and Manhattan
def searchAStarMax(state):
    print("\nSolving with max(Misplaced, Manhattan) heuristic...")
    puzzle = EightPuzzle(state)
    start_time = time.time()
    tupleSolution = astarSearch(puzzle, maxMisplacedManhattan)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)

def printHeuristicResults(tupleSolution, elapsed_time):
    print("--> Elapsed time: " + str(round(elapsed_time, 4)) + " seconds")
    print("--> Solution length: " + str(len(tupleSolution[0].solution())) + " tiles moved")
    print("--> Nodes removed from frontier: " + str(tupleSolution[1]))

#---------------------------------------------------- Question 3 ----------------------------------------------------#

# ~~ Creating Puzzle Object ~~ #
# copied from EightPuzzle and modified to fit new grid style
class DuckPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a board shaped like
            1 2
            3 4 5 6
              7 8 * """

    def __init__(self, initial=(1,2,3,4,5,6,7,8,0), goal=(1,2,3,4,5,6,7,8,0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment 
            0 1
            2 3 4 5
              6 7 8"""

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square in [2, 6, 7, 8]:
            possible_actions.remove('DOWN')
        if index_blank_square in [0, 1, 4, 5]:
            possible_actions.remove('UP')
        if index_blank_square in [1, 5, 8]:
            possible_actions.remove('RIGHT')
        if index_blank_square in [0, 2, 6]:
            possible_actions.remove('LEFT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        # movement changes based on where the blank tile is
        if (blank < 3):
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif (blank == 3):
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

# create and shuffle Duck Puzzle
def makeRandomDuckPuzzle():
    puzzle = DuckPuzzle()
    puzzle = shufflePuzzle(puzzle)
    #print("Shuffled Duck Puzzle")
    return puzzle

# ~~ DuckPuzzle Heuristics ~~ #

def ManhattanHeuristicDuck(node):
    #pre-computed Manhattan estimation - modified for Duck Puzzle
    listEstimation = [
        (0,1,1,2,3,4,3,4,5),
        (1,0,1,1,2,3,2,3,4),
        (1,2,0,1,2,3,2,3,4),
        (2,1,1,0,1,2,1,2,3),
        (3,2,2,1,0,1,2,1,2),
        (4,3,3,2,1,0,3,2,1),
        (3,2,2,1,2,3,0,1,2),
        (4,3,3,2,1,2,1,0,1),
        (5,4,4,3,2,1,2,1,0)
    ]
    
    #track total cost of node
    cost = 0
    #track current position of nodeTile in grid
    tilePosition = 0
    # nodeTile = the value of the tile in grid (0-8)
    for nodeTile in node.state:
        # tile home position is 1 index left of tile value
        # 0 tile shouldn't be counted in heuristic
        if nodeTile != 0:
            tileHomePosition = nodeTile - 1
            cost += listEstimation[tileHomePosition][tilePosition]
        
        tilePosition += 1
    return cost

# max of Misplaced Tile and Manhattan Heuristic
def maxMisplacedManhattanDuck(node):
    return max(ManhattanHeuristicDuck(node), MisplacedTileHeuristic(node))

# ~~ A* Calls ~~ #

def searchAStarMisplacedTileDuck(state):
    print("\nSolving with Misplaced Tile heuristic...")
    puzzle = DuckPuzzle(state)
    start_time = time.time()
    # [0] = node, [1] = # of nodes popped from frontier
    tupleSolution = astarSearch(puzzle, MisplacedTileHeuristic)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)

def searchAStarManhattanDuck(state):
    print("\nSolving with Manhattan heuristic...")
    puzzle = DuckPuzzle(state)
    start_time = time.time()
    tupleSolution = astarSearch(puzzle, ManhattanHeuristicDuck)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)

#search using max of Misplaced Tile and Manhattan
def searchAStarMaxDuck(state):
    print("\nSolving with max(Misplaced, Manhattan) heuristic...")
    puzzle = DuckPuzzle(state)
    start_time = time.time()
    tupleSolution = astarSearch(puzzle, maxMisplacedManhattanDuck)
    elapsed_time = time.time() - start_time
    printHeuristicResults(tupleSolution, elapsed_time)

def displayDuck(state):
    puzzle = DuckPuzzle(state)
    strRow = ""
    for i in range(9):
        #replace 0 with *
        if puzzle.initial[i] == 0:
            strRow += "*" + " "
        else:
            strRow += str(puzzle.initial[i]) + " "

        #check for last char in row & print
        if (i == 1):
            print(strRow)
            strRow = ""
        elif (i == 5):
            print(strRow)
            strRow = "  "
        elif (i == 8):
            print(strRow)
        

#----------- Global Space -----------#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Question 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Generate and solve 10 EightPuzzle objects

print("\n# ------------ Solving EightPuzzle ------------ #")

# #single trial:
# puzzle = EightPuzzle((1,0,4,8,3,2,7,5,6))
# listEightPuzzle = [puzzle]

listEightPuzzle = []
for i in range(10):
    eightPuzzle = make_rand_8puzzle()
    listEightPuzzle.append(eightPuzzle)

counter = 1
for puzzle in listEightPuzzle:
    print("\nSolving Puzzle #" + str(counter) + ":")
    counter += 1

    display(puzzle.initial)
    
    # search using Misplaced Tile heuristic
    searchAStarMisplacedTile(puzzle.initial)

    #search using Mahattan heuristic
    searchAStarManhattan(puzzle.initial)

    #search using max of Manhattan and Misplaced Tile
    searchAStarMax(puzzle.initial)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Question 3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Generate and solve 10 DuckPuzzle objects

print("\n# ------------ Solving DuckPuzzle ------------ #")

listDuckPuzzle = []
for i in range(10):
    duckPuzzle = makeRandomDuckPuzzle()
    listDuckPuzzle.append(duckPuzzle)

counter = 1
for puzzle in listDuckPuzzle:
    print("\nSolving Puzzle #" + str(counter) + ":")
    counter += 1

    displayDuck(puzzle.initial)

    # search using Misplaced Tile heuristic
    searchAStarMisplacedTileDuck(puzzle.initial)

    # search using Mahattan heuristic
    searchAStarManhattanDuck(puzzle.initial)

    # search using max of Manhattan and Misplaced Tile
    searchAStarMaxDuck(puzzle.initial)

#a1.py

from search import *
import time

#python passing info
# **modifying** a passed object will act as pass by reference
# **reassigning** a passed object will act as pass by value

#--- Question 1 ---#
# shuffle the 8-puzzle by starting with the goal
# and making a random number of random legal moves
def shufflePuzzle(puzzle):
    #move a random number of times
    numMoves = random.randint(151, 200)
    for x in range(numMoves):
        actions = puzzle.actions(puzzle.initial)
        randChoice = random.randint(0, len(actions)-1)
        newState = puzzle.result(puzzle.initial, actions[randChoice])
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


#--- Question 2 ---#

#seach using Misplaced Tile heuristic
def searchAStarMisplacedTile(state):
    print("Solving with heuristic: Misplaced Tile")
    puzzle = EightPuzzle(state)
    start_time = time.time()
    # TODO modify A* algorithm to display total number of tiles moved and total number of tiles remaining in frontier
    nodeSolution = astar_search(puzzle, display = True)
    elapsed_time = time.time() - start_time
    print("Elapsed time for Misplaced Tile Heuristic: " + str(round(elapsed_time, 2)) + " seconds")
    #display(nodeSolution.state)


puzzle = make_rand_8puzzle()
display(puzzle.initial)

searchAStarMisplacedTile(puzzle.initial)

#search using Mahattan heuristic
#def searchAStarManhattan(puzzle):

#search using the max of Manhattan and Misplaced Tile heuristic
#def searchAStarMax(puzzle):

    

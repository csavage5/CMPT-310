#a1.py

from search import *

def createRandomTuple():
    sortedArray = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(sortedArray)
    return tuple(sortedArray)


def make_rand_8puzzle():
    #check solvability of createRandom8Tuple
    tuple = createRandomTuple()
    puzzle = EightPuzzle(tuple, goal = (1, 2, 3, 4, 5, 6, 7, 8, 0))

    while not puzzle.check_solvability(tuple):
        print("Generated 8-puzzle not solvable, trying again...")
        
        tuple = createRandomTuple()
        puzzle = EightPuzzle(tuple, goal = (1, 2, 3, 4, 5, 6, 7, 8, 0))
        
    print("Found solvable 8-puzzle")
    return puzzle


def display(state):
    strRow = ""
    for i in range(9):
        #replace 0 with *
        if state[i] == "0":
            strRow += "*"
        else:
            strRow += state[i]

        #check for last char in row & print
        if (i + 1) % 3 == 0:
            print(strRow)
            strRow = ""
        else:
            strRow += " "


    

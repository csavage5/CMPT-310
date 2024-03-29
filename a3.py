# Cameron Savage, 301310824
# cdsavage@sfu.ca
# CMPT 310, SU2020

from enum import Enum
import copy
import random

"""
Explanation for why AI loses against Player if Player goes first

Fork Case: AI will lose against a smart player if:
    -> Player goes first, AND
    -> Player (O tile) creates a fork case, i.e.:
        | O |   |   |
        |   | X |   |
        |   |   | O |

        Note: coordinates are laid out as:
            | 1 | 2 | 3 |
            | 4 | 5 | 6 |
            | 7 | 8 | 9 |

In this case, the AI should place an X on an edge (tile # 2, 4, 6, 8) 
to properly kill the fork case, i.e.:

    | O |   |   |      | O |   |   |      | O |   | X |
    | X | X |   |  =>  | X | X | O |  =>  | X | X | O | => DRAW
    |   |   | O |      |   |   | O |      |   |   | O |

Instead, the AI places an X in the corner, which, with a 
smart Player, leads to:

    | O |   |   |      | O |   | O |
    |   | X |   |  =>  |   | X |   |  Player is guaranteed to win  
    | X |   | O |      | X |   | O |  no matter what the AI does

The AI chooses the bad move because the random playouts see it as 
the best move. Without game knowledge or more criteria to evaluate 
the best position, the AI can only decide on a move based on the 
knowledge it has. When deciding for this move:
    | O |   |   |
    |   | X |   |
    |   |   | O |

    The results the AI gets from the playouts are:
        Move #0:
        --> Coordinate: 2
        --> Wins: 1690, Losses: 1353, Draws: 342
        --> Evaluation Metric: 1.500738552437223
        Move #1:
        --> Coordinate: 3
        --> Wins: 1795, Losses: 1270, Draws: 328
        --> Evaluation Metric: 1.6703383162863887
        Move #2:
        --> Coordinate: 4
        --> Wins: 1631, Losses: 1322, Draws: 362
        --> Evaluation Metric: 1.5064247921390779
        Move #3:
        --> Coordinate: 6
        --> Wins: 1698, Losses: 1299, Draws: 355
        --> Evaluation Metric: 1.5792307692307692
        Move #4:
        --> Coordinate: 7
        --> Wins: 1758, Losses: 1226, Draws: 297
        --> Evaluation Metric: 1.6748166259168704
        Move #5:
        --> Coordinate: 8
        --> Wins: 1649, Losses: 1317, Draws: 308
        --> Evaluation Metric: 1.484825493171472
        ** Chose Move #4 **

        Note: 
        -> Move is chosen based on the *largest* evaluation metric
        -> Evaluation metric is win + draw : loss ratio

The AI *should* have chosen Move # 0, 2, 3, or 8, but those all were evaluated
as worse than Move #4, which is the corner move. I have modified the evaluation
metric, but still end up with the same result.

The AI will always choose the bad move because the bad move is always evaluated
as better based on the purely random playouts (i.e. Pure Monte Carlo Tree Search).
In order to fix this we would have to add a heuristic, like Upper Confidence Bound,
to choose moves in the playouts instead of randomness - which is against the rules
of the assignment. 

If the AI goes first, the AI will shut down the player's attempt to make the fork
case:

|   |   |   |      | O |   |   |      | O |   |   |      | O |   |   |      | O |   | X |
|   | X |   |  =>  |   | X |   |  =>  | X | X |   |  =>  | X | X | O |  =>  | X | X | O |  =>  DRAW
|   |   |   |      |   |   |   |      |   |   |   |      |   |   |   |      |   |   |   |

If the AI goes first, the AI will always win or draw against a smart player.

"""

class Turn(Enum):
    NONE = 0
    CPU = 1
    PLAYER = 2

class BoardState():
    
    def __init__(self, turn: Turn, board: list = [0] * 9):
        self.board = board
        self.validMoves = [0] * 9
        self.calcValidMoves()
        self.turn = turn
        self.filled = False
        self.victor = Turn.NONE
        self.lastMove = 0

    # duplicates given BoardState to this instance
    def update(self, boardState):
        self.board = copy.deepcopy(boardState.board)
        self.calcValidMoves()
        self.turn = boardState.turn
        self.filled = boardState.filled
        self.victor = boardState.victor
        self.lastMove = boardState.lastMove

    def printBoard(self):
        index = 0
        boardString = ""
        for tile in self.board:
            if tile == 0:
                # empty
                #boardString += str("| " + str(index + 1) + " ")
                boardString += str("|   ")
            elif tile == 1:
                # X
                boardString += str("| X ")
            elif tile == 2:
                # 0
                boardString += str("| O ")
            
            if (index + 1) % 3 == 0:
                boardString += '|\n'

            index += 1

        print(boardString)

    def isValidMove(self, choice: int):
        if (choice < 0 or choice >= len(self.validMoves)):
            return False

        return (self.validMoves[choice] == 1)

    def isGameOver(self) -> bool:
        return (self.filled or self.victor != Turn.NONE)
    
    # Generate moves from current board, as BoardStates
    def getChildrenStates(self) -> list:
        # generate children
        childList = []
        index = 0

        # verify state is not won
        if self.isGameOver():
            return childList

        for x in self.validMoves:
            if x == 1:
                # position is available
                newBoard = BoardState(self.turn, copy.deepcopy(self.board))
                newBoard.makeMove(index)
                
                childList.append(newBoard)
                
            index += 1

        return childList  

    # Generate moves from current board, as mcNodes
    def getChildrenNodes(self) -> list:
        childList = []
        index = 0
        for x in self.validMoves:
            if x == 1:
                # position is available
                newBoard = BoardState(self.turn, copy.deepcopy(self.board))
                newBoard.makeMove(index)
                
                childList.append(mcNode(newBoard))
                
            index += 1

        return childList  

    # Checks if current board is a victory for
    # the player in self.turn
    def checkVictory(self):

        foundVictory = False
        # check diagonal
        for diag in range(0, 3, 2):
            counter = 0
            for offset in range(3):
                coordinate = diag + ( (4 - diag) * offset)
                #print(str(coordinate))
                if self.board[coordinate] == self.turn.value:
                    counter += 1
            
            if counter == 3:
                #print("found diagonal victory")
                foundVictory = True

        # check horizontal
        if not foundVictory:
            for row in range(3):
                counter = 0
                for col in range(3):
                    if self.board[self.convert(col, row)] == self.turn.value:
                        counter += 1
                
                if counter == 3:
                    foundVictory = True

        #check vertical
        if not foundVictory:
            for col in range(3):
                counter = 0
                for row in range(3):
                    if self.board[self.convert(col, row)] == self.turn.value:
                        counter += 1
                
                if counter == 3:
                    foundVictory = True

        if foundVictory:
            self.victor = self.turn

    def switchTurn(self):
        if self.turn == Turn.PLAYER:
            #print("Switching turn to CPU")
            self.turn = Turn.CPU
        elif self.turn == Turn.CPU:
            #print("Switching turn to PLAYER")
            self.turn = Turn.PLAYER

    def makeRandomMove(self):
        validMoveIndex = []

        index = 0
        for x in self.validMoves:
            if x == 1:
                validMoveIndex.append(index)
            index += 1

        #get random validMove
        position = random.choice(validMoveIndex)
        self.makeMove(position)

    # Places an X or an O at position, depending on
    # the value of self.turn
    def makeMove(self, position: int):
        if self.filled == False and self.victor == Turn.NONE:
            if self.turn == Turn.PLAYER:
                # place player tile - O
                self.board[position] = Turn.PLAYER.value

            elif self.turn == Turn.CPU:
                # place CPU tile - X
                self.board[position] = Turn.CPU.value
            
            # recalculate validMoves
            self.calcValidMoves()
            self.checkVictory()
            self.switchTurn()
            self.lastMove = position

        else:
            print("Cannot move, game end condition(s) is/are met")

    # Saves which spaces on the board are empty
    def calcValidMoves(self):
        index = 0
        counter = 0
        for tile in self.board:
            if tile == 0:
                self.validMoves[index] = 1
                counter += 1
            elif tile > 0:
                self.validMoves[index] = 0
            index += 1

        if counter == 0:
            self.filled = True
                
    def convert(self, x: int, y:int) -> int:
        return (y * 3) + x


class mcNode():
    def __init__(self, state : BoardState):
        self.state = state
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.evalMetric = 0

    def update(self, newNode):
        self.state.update(newNode.boardState)
        self.id = newNode.id
        self.wins = newNode.wins
        self.losses = newNode.losses
        self.draws = newNode.draws
        self.moveCoordinate = newNode.moveCoordinate

    def updateEvalMetric(self):
        #self.evalMetric = self.wins + self.draws
        #self.evalMetric = self.losses * -1
        #self.evalMetric = self.draws
        
        # add 1 to losses to avoid divide by 0 error
        self.evalMetric = (self.wins + self.draws) / (self.losses + 1)

    def completeRandomPlayout(self):        
        # get children of state
        children = self.state.getChildrenStates()

        # if no children, board is full
        if len(children) > 0:
            # randomly choose a child state
            #print("Size of children: " + str(len(children)))
            child = random.choice(children)

            # while the state is not in endgame, 
            # keep making random moves
            while (not child.isGameOver()):
                child.makeRandomMove()
        
        else:
            child = self.state

        # add statistics to node based on victor
        #self.playouts += 1

        if child.victor == Turn.PLAYER:
            self.losses += 1
        elif child.victor == Turn.CPU:
            self.wins += 1
        elif child.victor == Turn.NONE:
            self.draws += 1

        self.updateEvalMetric()

class TTTGame():

    def __init__(self, turn : Turn):
        self.state = BoardState(turn, [0] * 9)

    def CPUMove(self):
        print("CPU is making a move...")

        subnodes = self.state.getChildrenNodes()

        # complete a large number of random playouts
        random.seed()
        for _ in range(10000):
            childChoice = random.choice(subnodes)
            childChoice.completeRandomPlayout()

        # TODO analyze child moves of node, decide which one is best
        # choose a move
        index = 0
        maxMetric = 0
        childIndex = 0
        for child in subnodes:
            print("Move #" + str(index) + ":")
            print("--> Coordinate: " + str(child.state.lastMove + 1))
            print("--> Wins: " + str(child.wins) + ", Losses: " + str(child.losses) + ", Draws: " + str(child.draws))
            print("--> Evaluation Metric: " + str(child.evalMetric))

            if child.evalMetric > maxMetric:
                maxMetric = child.evalMetric
                childIndex = index

            elif child.evalMetric == maxMetric:
                # if there's a tie, resolve via coin flip
                if random.randint(0, 1) == 0:
                    maxMetric = child.evalMetric
                    childIndex = index

            index += 1

        print("** Chose Move #" + str(childIndex) + " **\n")
        # update state with state of child
        self.state.update(subnodes[childIndex].state)
        self.state.printBoard()

    def playerMove(self):
        choice = int(input("Place O at coordinate: ")) - 1

        while (not self.state.isValidMove(choice)):
            choice = int(input("Invalid choice, pick again: ")) - 1

        self.state.makeMove(choice)
        self.state.printBoard()
    

def play_a_new_game():
    
    userInput = input(
'''
Welcome to Tic-Tac-Toe! You are Os, the CPU is Xs.

Enter 1 to go first, enter 2 to go second: ''')

    print('''
When prompted to place an O, enter the number that matches the desired placement.
    | 1 | 2 | 3 |
    | 4 | 5 | 6 |
    | 7 | 8 | 9 |
    ''')

    turn = Turn.CPU
    
    if userInput == "1":
        turn = Turn.PLAYER
    elif userInput == "2":
        turn = Turn.CPU

    game = TTTGame(turn)

    while (not game.state.isGameOver()):
        print("is now " + game.state.turn.name + "'s turn")
        if game.state.turn == Turn.PLAYER:
            # player makes a move
            game.playerMove()

        else:
            # CPU makes a move
            game.CPUMove()

    # update game status
    print("Game is over - the winner is " + game.state.victor.name)

    # ~testing~
    # state = BoardState(Turn.CPU, [1,0,0, 0,1,0, 0,0,1])
    # state.checkVictory()
    # game.state.makeMove(0)
    # game.state.makeMove(1)
    # game.state.makeMove(3)
    # game.state.makeMove(4)
    # game.state.makeMove(6)
    # game.state.makeMove(8)
    # #game.board.calcValidMoves()
    # #game.board.checkVictory()
    # print(game.state.victor)

if __name__ == "__main__":
    play_a_new_game()

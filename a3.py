from enum import Enum
import copy
import random

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

    def update(self, boardState):
        self.board = copy.deepcopy(boardState.board)
        self.calcValidMoves()
        self.turn = boardState.turn
        self.filled = boardState.filled
        self.victor = boardState.victor

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
        return (self.validMoves[choice] == 1)

    def isGameOver(self) -> bool:
        return (self.filled or self.victor != Turn.NONE)

    def getChildrenStates(self) -> list:
        # generate children
        childList = []
        index = 0
        for x in self.validMoves:
            if x == 1:
                # position is available
                newBoard = BoardState(self.turn, copy.deepcopy(self.board))
                newBoard.makeMove(index)
                
                childList.append(newBoard)
                
            index += 1

        return childList  

    def getChildrenNodes(self) -> list:
        # generate children
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

    def checkVictory(self):
        #check diagonal
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
        #get random validMove
        validMoveIndex = []

        index = 0
        for x in self.validMoves:
            if x == 1:
                validMoveIndex.append(index)
            index += 1

        position = random.choice(validMoveIndex)
        self.makeMove(position)

    def makeMove(self, position: int):
        if self.filled == False and self.victor == Turn.NONE:
            if self.turn == Turn.PLAYER:
                # place player tile - O
                #print("Placing PLAYER tile")
                self.board[position] = Turn.PLAYER.value

            elif self.turn == Turn.CPU:
                # place CPU tile - X
                #print("Placing CPU tile")
                self.board[position] = Turn.CPU.value
            
            # recalculate validMoves
            self.calcValidMoves()
            self.checkVictory()
            #self.printBoard()
            self.switchTurn()

        else:
            print("Cannot move, game end condition(s) is/are met")

    def calcValidMoves(self):
        index = 0
        counter = 0
        for tile in self.board:
            # print("tile: " + str(tile))
            if tile == 0:
                self.validMoves[index] = 1
                counter += 1
            elif tile > 0:
                self.validMoves[index] = 0
            index += 1
        #print("valid moves: " + str(self.validMoves))
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
        self.playouts = 0
        self.evalMetric = 0

    def update(self, newNode):
        self.state.update(newNode.boardState)
        self.id = newNode.id
        self.wins = newNode.wins
        self.losses = newNode.losses
        self.draws = newNode.draws
        self.moveCoordinate = newNode.moveCoordinate

    def updateEvalMetric(self):
        self.evalMetric = self.wins + self.draws
        #self.evalMetric = self.losses * -1

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
        self.playouts += 1

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
        self.tree = dict()
        self.nodeCounter = 0

    def CPUMove(self):
        print("CPU is making a move...")
        #print("valid moves: " + str(self.state.validMoves))

        subnodes = self.state.getChildrenNodes()

        # complete a large number of random playouts
        for _ in range(20000):
            childChoice = random.choice(subnodes)
            childChoice.completeRandomPlayout()

        # TODO analyze child moves of node, decide which one is best
        # choose a move
        index = 0
        maxMetric = 0
        childIndex = 0
        for child in subnodes:
            if child.evalMetric > maxMetric:
                maxMetric = child.evalMetric
                childIndex = index

            index += 1

        # update state with state of child
        self.state.update(subnodes[childIndex].state)
        self.state.printBoard()
        #print("valid moves: " + str(self.state.validMoves))


    def playerMove(self):
        choice = int(input("Place O at coordinate: ")) - 1

        while (not self.state.isValidMove(choice)):
            choice = int(input("Invalid choice, pick again: ")) - 1

        self.state.makeMove(choice)
        #print("valid moves: " + str(self.state.validMoves))
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

    # #testing
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

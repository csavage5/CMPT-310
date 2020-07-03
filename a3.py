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
        self.finished == False

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
                boardString += str("  ")
            elif tile == 1:
                # X
                boardString += str("X ")
            elif tile == 2:
                # 0
                boardString += str("O ")
            
            if (index + 1) % 3 == 0:
                boardString += '\n'

            index += 1

        print(boardString)

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
        for diag in range(2, -1, 2):
            counter = 0
            for offset in range(3):
                coordinate = diag + ( (4 - diag) * offset)
                if self.board[coordinate] == self.turn.value:
                    counter += 1
            
            if counter == 3:
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
            self.finished = True

    def switchTurn(self):
        if self.turn == Turn.PLAYER:
            print("Switching turn to CPU")
            self.turn = Turn.CPU
        elif self.turn == Turn.CPU:
            print("Switching turn to PLAYER")
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
                print("Placing PLAYER tile")
                self.board[position] = Turn.PLAYER.value

            elif self.turn == Turn.CPU:
                # place CPU tile - X
                print("Placing CPU tile")
                self.board[position] = Turn.CPU.value
            
            # recalculate validMoves
            self.calcValidMoves()
            self.checkVictory()
            self.printBoard()
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
        print("valid moves: " + str(self.validMoves))
        if counter == 0:
            self.filled = True
            self.finished = True
                
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
        self.evalMetric = self.wins

    def completeRandomPlayout(self):
        # get children of state
        children = self.state.getChildrenStates()
        # randomly choose a child state
        child = random.choice(children)

        # while the state is not in endgame, 
        # keep making random moves
        while (not child.finished):
            child.makeRandomMove()
        
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
        self.state = BoardState(Turn.CPU, [0] * 9)
        self.tree = dict()
        self.nodeCounter = 0

    def CPUMove(self):
        print("CPU is making a move...")

        subnodes = self.state.getChildrenNodes()

        # complete a large number of random playouts
        for _ in range(500):
            childChoice = random.choice(subnodes)
            childChoice.completeRandomPlayout()

        # TODO analyze child moves of node, decide which one is best
        # choose node with highest win + draw stat if there is more than 1 move with the same # of wins
        mostWinsIndex = 0
        mostWins = 0
        winDuplicates = True

        index = 0
        for child in children:
            if child.wins > mostWins:
                mostWinsIndex = index
                mostWins = child.mostWins
                winDuplicates = False

            elif child.wins == mostWins:
                winDuplicates = True

            index += 1

        self.board.makeMove(children[mostWinsIndex].moveCoordinate)

    def playerMove(self):
        self.state.printBoard()
        choice = input("Place X at coordinate: ")
        self.state.makeMove(choice)
    

def play_a_new_game():
    
    #userInput = input("Welcome to Tic-Tac-Toe! You are X's, the CPU is O's.\nEnter 1 to go first, enter 2 to go second: ")
    turn = Turn.CPU
    # if userInput == "1":
    #     turn = Turn.PLAYER
    # elif userInput == "2":
    #     turn = Turn.CPU

    game = TTTGame(turn)

    # testing
    game.state.makeMove(0)
    game.state.makeMove(1)
    game.state.makeMove(3)
    game.state.makeMove(4)
    game.state.makeMove(6)
    game.state.makeMove(8)
    #game.board.calcValidMoves()
    #game.board.checkVictory()
    print(game.state.victor)


    # while game.board.isGameOver() == False:
    #     print("is now " + game.board.turn.name + "'s turn")
    #     if game.board.turn == Turn.PLAYER:
    #         # player makes a move
    #         game.playerMove()
    #         #game.turn = Turn.CPU

    #     else:
    #         # CPU makes a move
    #         game.CPUMove()

    # update game status


if __name__ == "__main__":
    play_a_new_game()

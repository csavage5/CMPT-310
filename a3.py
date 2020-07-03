from enum import Enum
import copy

class Turn(Enum):
    NONE = 0
    CPU = 1
    PLAYER = 2

class BoardState():
    
    def __init__(self, turn: Turn, board: list):
        self.board = board
        self.validMoves = [0] * 9
        self.calcValidMoves()
        self.turn = turn
        self.filled = False
        self.victor = Turn.NONE

    def update(self, board):
        self.board = copy.deepcopy(board.board)
        self.calcValidMoves()
        self.turn = board.turn
        self.filled = board.filled
        self.victor = board.victor

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

    def checkVictory(self):

        #check diagonal
        # if lastPlacement in corners
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
            counter = 0
            for row in range(3):
                for col in range(3):
                    if self.board[self.convert(col, row)] == self.turn.value:
                        counter += 1
                
                if counter == 3:
                    foundVictory == True

        #check vertical
        if not foundVictory:
            counter = 0
            for col in range(3):
                for row in range(3):
                    if self.board[self.convert(col, row)] == self.turn.value:
                        counter += 1
                
                if counter == 3:
                    foundVictory == True

        if foundVictory:
            self.victor = self.turn

    def switchTurn(self):
        if self.turn == Turn.PLAYER:
            self.turn == Turn.CPU
        else:
            self.turn == Turn.PLAYER

    def makeMove(self, position: int):
        if self.filled == False and self.victor == Turn.NONE:
            if self.turn == Turn.PLAYER:
                # place player tile - O
                self.board[position] = Turn.PLAYER.value

            else:
                # place CPU tile - X
                self.board[position] = Turn.CPU.value
            
            # recalculate validMoves
            self.calcValidMoves()
            self.checkVictory()
            self.printBoard()
            self.switchTurn()

    def calcValidMoves(self):
        index = 0
        counter = 0
        for tile in self.board:
            if tile == 0:
                self.validMoves[index] = 1
                counter += 1
            index += 1
        #print("valid moves: " + str(self.validMoves))
        if counter == 0:
            self.filled = True
                
    def convert(self, x: int, y:int) -> int:
        return (y * 3) + x


class mcNode():

    def __init__(self, id : int, board : BoardState, moveCoordinate = -1):
        self.boardState = board
        self.id = id
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.moveCoordinate = moveCoordinate

    def update(self, newNode):
        self.boardState.update(newNode.boardState)
        self.id = newNode.id
        self.wins = newNode.wins
        self.losses = newNode.losses
        self.draws = newNode.draws
        self.moveCoordinate = newNode.moveCoordinate


class TTTGame():

    def __init__(self, turn : Turn):
        self.board = BoardState(Turn.CPU, [0] * 9)
        self.tree = dict()
        self.nodeCounter = 0

    def CPUMove(self):
        print("CPU is making a move...")
        # call recursiveMonteCarlo on each child board
        # to get total data for each possible move
        self.tree.clear()
        self.nodeCounter = 0
        node = mcNode(0, copy.deepcopy(self.board))
        node = self.recursiveMonteCarlo(copy.deepcopy(node))
        print("-------------------------DONE -----------------------------------")
        # TODO analyze child moves of node, decide which one is best
        # choose node with highest win + draw stat if there is more than 1 move with the same # of wins
        mostWinsIndex = 0
        mostWins = 0
        winDuplicates = True
        #print(self.tree)
        children = self.tree.get(node.id)
        index = 0
        for child in children:
            if child.wins > mostWins:
                mostWinsIndex = index
                mostWins = child.mostWins
                winDuplicates = False

            elif child.wins == mostWins:
                winDuplicates = True

            index += 1

        # break wins tie
        # if winDuplicates:
        #     winsAndDraws = 0
        #     for child in children:
        #         if child.wins == mostWins and (child.wins + child.draws > winsAndDraws):

        self.board.makeMove(children[mostWinsIndex].moveCoordinate)

    def playerMove(self):
        self.board.printBoard()
        choice = input("Place X at coordinate: ")
        self.board.makeMove(choice)
    
    def recursiveMonteCarlo(self, node: mcNode) -> mcNode: 
        
        # base case - node.boardState.victory == true, update win / loss data
        if node.boardState.victor != Turn.NONE or node.boardState.filled == True:
            print("base case")
            if node.boardState.victor == Turn.PLAYER:
                # record LOSS
                node.losses += 1
            elif node.boardState.victor == Turn.CPU:
                # record WIN
                node.wins += 1
            elif node.boardState.victor == Turn.NONE:
                # board is filled, record DRAW
                node.draws += 1
            return copy.deepcopy(node)

        # generate children
        childList = []
        index = 0
        print(node.boardState.board)
        print(node.boardState.validMoves)
        for x in node.boardState.validMoves:
            if x == 1:
                # position is available
                newBoard = BoardState(node.boardState.turn, copy.deepcopy(node.boardState.board))
                newBoard.makeMove(index)
                
                self.nodeCounter += 1
                childList.append(mcNode(self.nodeCounter, newBoard, index))
                
            index += 1
        #print("******************* NODECOUNT " + str(self.nodeCounter))
        #call recursiveMonteCarlo for each child
        for index in range(len(childList)):
            childList[index].update(self.recursiveMonteCarlo(copy.deepcopy(childList[index])))
            #print(childList[index].id)

        # TODO total up data for children, save it to current node's data
        for child in childList:
            node.wins += child.wins
            node.losses += child.losses
            node.draws += child.draws

        # add children to tree
        self.tree.update({node.id: childList})

        return copy.deepcopy(node)


def play_a_new_game():
    
    userInput = input("Welcome to Tic-Tac-Toe! You are X's, the CPU is O's.\nEnter 1 to go first, enter 2 to go second: ")
    turn = Turn.CPU
    if userInput == "1":
        turn = Turn.PLAYER
    elif userInput == "2":
        turn = Turn.CPU

    game = TTTGame(turn)
    
    while game.board.isGameOver() == False:
        print("is now " + game.board.turn.name + "'s turn")
        if game.board.turn == Turn.PLAYER:
            # player makes a move
            game.playerMove()
            #game.turn = Turn.CPU

        else:
            # CPU makes a move
            game.CPUMove()

    # update game status


if __name__ == "__main__":
    play_a_new_game()

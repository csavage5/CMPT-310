from enum import Enum

class Turn(Enum):
    NONE = 0
    CPU = 1
    PLAYER = 2

class BoardState():
    
    def __init__(self, turn: Turn, board: list[int]):
        self.board = board
        self.validMoves = [0] * 9
        self.calcValidMoves()
        self.turn = turn
        self.filled = False
        self.victor = Turn.NONE

    def printBoard(self):
        index = 0
        boardString = ""
        for tile in board:
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
        print(boardString)

    def checkVictory(self, lastPlacement: int):
        #check if the last placed tile wins the game
        # corners = [0, 2, 6, 8]
        # centre = 4
        # edges = [1, 3, 5, 7]

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
                    if self.board[convert(col, row)] == self.turn.value:
                        counter += 1
                
                if counter == 3:
                    foundVictory == True

        #check vertical
        if not foundVictory:
            counter = 0
            for col in range(3):
                for row in range(3):
                    if self.board[convert(col, row)] == self.turn.value:
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
            if turn == Turn.PLAYER:
                # place player tile - O
                self.board[position] = Turn.PLAYER.value

            else:
                # place CPU tile - X
                self.board[position] = Turn.CPU.value
            
            # recalculate validMoves
            self.calcValidMoves()
            self.checkVictory(position)
            self.printBoard()
            self.switchTurn()

    def calcValidMoves(self):
        index = 0
        counter = 0
        for tile in board:
            if tile == 0:
                validMoves[index] == 1
                counter += 1
            index += 1

        if counter == 0:
            filled = True
                
    def convert(self, x: int, y:int) -> int:
        return (y * 3) + x


class mcNode():

    def __init__(self, id : int, board : State):
        self.boardState = board
        self.id = id
        self.wins = 0
        self.losses = 0
        self.draws = 0


class TTTGame():

    gameOver = False

    def __init__(self, turn : Turn):
        self.boardState = BoardState(Turn.CPU, [0] * 9)
        self.tree = dict()
        self.nodeCounter = 0

    def CPUMove(self):
        
        # call recursiveMonteCarlo on each child board
        # to get total data for each possible move
        self.tree.clear()
        self.nodeCounter = 0
        node = mcNode(0, self.boardState)
        recursiveMonteCarlo(node, 0)
        # analyze children of tree.get(0), decide which one is best
        childList = self.tree.get(0)
        # self.boardState.makeMove(bestMove)

    def promptPlayer(self):
        boardState.printBoard()
        choice = input("Place X at coordinate: ")
        boardState.makeMove(choice, Turn.PLAYER)
    
    def recursiveMonteCarlo(self, node: mcNode, nodeID: int) -> mcNode:
        
        # TODO base case - node.boardState.victory == true, update win / loss data
        if node.boardState.victor != Turn.NONE or node.boardState.filled == True:
            if node.boardState.victor == Turn.PLAYER:
                # record LOSS
                mcNode.losses += 1
            elif node.boardState.victor == Turn.CPU:
                # record WIN
                mcNode.wins += 1
            elif node.boardState.victor == Turn.NONE:
                # board is filled, record DRAW
                mcNode.draws += 1
            return mcNode

        # generate children
        childList = []
        index = 0
        for x in node.boardState.validMoves:
            if x == 1:
                # position is available
                newBoard = BoardState(node.boardState.turn, node.boardState.board)
                newBoard.makeMove(index)
                
                self.nodeCounter += 1
                childList.append(mcNode(nodeCounter, newBoard))
                
            index += 1

        # add children to tree
        
        
        #call recursiveMonteCarlo for each child
        for index in range(len(childList)):
            childList[index] = recursiveMonteCarlo(childList[index])

        self.tree.update(nodeID, childList)


def play_a_new_game():
    game = TTTGame(Turn.CPU)
    while game.gameOver == False:
        if game.turn == Turn.PLAYER:
            # player makes a move
            game.promptPlayer()
            game.turn = Turn.CPU

        else:
            # CPU makes a move
            game.CPUMove()
    
    # update game status

if __name__ == "__main__":
    play_a_new_game()

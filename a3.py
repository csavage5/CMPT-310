from enum import Enum

class Turn(Enum):
    PLAYER = 1
    CPU = 2


class State():
    
    def __init__(self, turn: Turn, board: list):
        self.board = board
        self.validMoves = [0] * 9
        self.calcValidMoves()
        self.turn = turn
        self.won = False

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

    def switchTurn(self):
        if self.turn == Turn.PLAYER:
            self.turn == Turn.CPU
        else:
            self.turn == Turn.PLAYER

    def makeMove(self, position: int):
        if turn == Turn.PLAYER:
            # place player tile - O
            self.board[position] = 2

        else:
            # place CPU tile - X
            self.board[position] = 1
        
        self.printBoard()
        # TODO check for victory
        # switch turn **if not victory** 
        self.switchTurn()
        # recalculate validMoves
        self.calcValidMoves()

    def calcValidMoves(self):
        index = 0
        for tile in board:
            if tile == 0:
                validMoves[index] == 1
            index += 1
                
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
        self.boardState = State(Turn.CPU, [0] * 9, [1] * 9)
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

    def recursiveMonteCarlo(self, node: mcNode, nodeID: int) -> mcNode:
        
        # TODO base case - node.boardState.victory == true, update win / loss data
        
        # generate children
        childList = []
        index = 0
        for x in node.boardState.validMoves:
            if x == 1:
                # position is available
                newBoard = State(node.boardState.turn, node.boardState.board)
                newBoard.makeMove(index)
                
                self.nodeCounter += 1
                childList.append(mcNode(nodeCounter, newBoard))
                
            index += 1

        # add children to tree
        self.tree.update(nodeID, childList)
        
        #call recursiveMonteCarlo for each child
        for index in len(childList):
            childList[index] = recursiveMonteCarlo(childList[index])



    def promptPlayer(self):
        boardState.printBoard()
        choice = input("Place X at coordinate: ")
        boardState.makeMove(choice, Turn.PLAYER)

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

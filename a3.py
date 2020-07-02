from enum import Enum

class Turn(Enum):
    PLAYER = 1
    CPU = 2


class State():
    
    def __init__(self, turn : Turn, board, validMoves):
        self.board = board
        #self.validMoves = validMoves
        self.validMoves = [0] * 9
        self.calcAvailableMoves()
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

    def makeMove(self, turn : Turn):
        if turn == Turn.PLAYER:
            # place player tile

        else:
            # place CPU tile

    def calcAvailableMoves(self):
        index = 0
        for tile in board:
            if tile == 0:
                validMoves[index] == 1
            index += 1
                

    def convert(self, x: int, y:int) -> int:
        return (y * 3) + x


class mcNode():
    
    self.wins = 0
    self.losses = 0
    self.draws = 0

    def __init__(self, turn : Turn, id : int, board, validMoves):
        boardState = State(turn, board, validMoves)
        self.id = id

class TTTGame():

    gameOver = False

    def __init__(self, turn : Turn):
        self.boardState = State(Turn.CPU, [0] * 9, [1] * 9)

    def CPUMove(self):
        tree = dict()
        # call recursiveMonteCarlo on each child board
        # to get total data for each possible move

        def recursiveMonteCarlo(nodeID: int):
            childList = []
            # for x in range(# of 1's in boardState.validMoves)...
            #   childList.append(mcNode(State(with tile placed at board[x])))
            
            tree.update(nodeID, childList)

            for child in childList:


        recursiveMonteCarlo(0)
        # analyze children of tree.get(0), decide which one is best
        # self.boardState.makeMove(bestMove)

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

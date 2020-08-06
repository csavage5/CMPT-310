package cmpt310.a5.model;

public class Game {

    public Board board;

    private Agent player1;
    private Agent player2;

    public Game(Agent player1, Agent player2) {
        board = new Board();
        this.player1 = player1;
        this.player2 = player2;
    }

    public void startGame() {

        takeTurn();

        // check if game is over


    }

    public void takeTurn() {

        // TODO deal with case where player passes turn
        //  because no valid moves

        board.discoverValidMoves();

        int moveLocation = -1;

        if (board.state == Board.Turn.PLAYER1) {
            moveLocation = player1.makeMove(board);
        } else if (board.state == Board.Turn.PLAYER2) {
            moveLocation = player2.makeMove(board);
        }

        board.selectValidMove(moveLocation);

    }
}

package cmpt310.a5.model;

public class Game {

    public enum Turn {
        PLAYER1,
        PLAYER2,
        FINISHED
    }

    private Enum<Turn> state;
    private Board board;

    public Game() {
        board = new Board();

    }

    public Board getBoard() {
        return board;
    }

}

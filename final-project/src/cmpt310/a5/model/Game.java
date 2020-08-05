package cmpt310.a5.model;

public class Game {

    public enum Turn {
        PLAYER1,
        PLAYER2,
        FINISHED
    }

    private Enum<Turn> state;
    private Board board;

    private Agent player1;
    private Agent player2;

    public Game(Agent player1, Agent player2) {
        board = new Board();
        this.player1 = player1;
        this.player2 = player2;
    }

    public Board getBoard() {
        return board;
    }

}

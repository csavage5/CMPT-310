package cmpt310.a5.model;

public abstract class Agent {

    private Board.Turn playerNumber;

    public Agent(Board.Turn playerNumber) {
        this.playerNumber = playerNumber;
    }

    /**
     * Given a board, returns the position to
     * make a move at
     * @param board
     * @return coordinate for move
     */
    public abstract int makeMove(Board board);


}

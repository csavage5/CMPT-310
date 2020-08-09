package cmpt310.a5.model;

public class Game {

    public Board board;

    private Agent[] players = new Agent[2];

    private Agent player1;
    private Agent player2;

    public Game(Agent player1, Agent player2) {
        board = new Board();
        this.players[0] = player1;
        this.players[1] = player2;
    }

    // TODO check if game is over

    public void takeTurn() {

        int moveLocation = -1;

        // re-prompt player for move selection if invalid
        while (true) {
            try {
                board.selectValidMove(players[board.getStateValue()].makeMove(board));

            } catch (IllegalArgumentException e) {
                //System.out.println("Error: selected invalid coordinate, please try again.\n");
                System.out.println(e.getMessage());
                continue;
            }

            break;
        }


    }

    public boolean discoverValidMoves() {
        // TODO deal with case where player passes turn
        //  because no valid moves
        return board.discoverValidMoves();
    }

    public boolean isGameFinished() {
        return (board.isGameOver());
    }

    /**
     * Resets game board to starting state
     */
    public void reset() {
        board = new Board();
    }

}

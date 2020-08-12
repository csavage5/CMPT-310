package cmpt310.a5.controller;

import cmpt310.a5.model.*;
import cmpt310.a5.view.*;

/**
 * Receives user input and sends the Model commands based on that input.
 * Receives results from Model and tells the View what to display.
 */
public class GameController {
    public int MAX_GAME_LOOPS;
    private Game game;
    private int gamesWonP1 = 0;
    private int gamesWonP2 = 0;
    private int gamesDrawn = 0;


    public GameController() {

        Integer[] selection = TextOutput.selectPlayerPrompt();
        game = new Game(getAgentTypeFromInput(selection[0], Board.Turn.PLAYER1),
                getAgentTypeFromInput(selection[1], Board.Turn.PLAYER2));

        MAX_GAME_LOOPS = selection[2];

        gameLoop();
    }

    private void gameLoop() {

        while (!game.isGameFinished()) {

            if (game.discoverValidMoves()) {
                // player doesn't skip turn
                TextOutput.printBoard(game.board.getGameBoardWithValidMoves());
                TextOutput.printTurnInformation(game.board.state,
                        game.board.getScoreP1(), game.board.getScoreP2());
                game.takeTurn();
            } else {
                //player skips turn, output different UI message
                TextOutput.printSkippedTurn(game.board.state.getOpposite());
            }
        }

        //Display reason for game ending
        TextOutput.printBoard(game.board.getGameBoard());
        if (game.board.didBothPlayersSkip()) {
            System.out.println("Game ended: both players could not place a tile.");
        } else if (game.board.isBoardFilled()) {
            System.out.println("Game ended: game board is filled.");
        }

        // record win
        switch (game.board.victor) {
            case PLAYER1:
                gamesWonP1++;
                break;
            case PLAYER2:
                gamesWonP2++;
                break;
            case TIE:
                gamesDrawn++;
                break;
        }

        TextOutput.printGameOver(game.board.victor, game.board.getScoreP1(), game.board.getScoreP2());
        System.out.println("Totals: P1 - " + gamesWonP1 + "; P2 - " + gamesWonP2 + "; Draws: " + gamesDrawn);


        if (gamesWonP1 + gamesWonP2 + gamesDrawn < MAX_GAME_LOOPS) {
            game.reset();
            System.out.println("Starting new game...\n");
            gameLoop();
        }

    }

    /**
     * Prompts user for coordinate
     * @return index of move
     */
    public static int promptUserForCoordinate() {
        return Position.convertLetterNumber(TextOutput.promptCoordinateEntry());
    }

    private Agent getAgentTypeFromInput(Integer input, Board.Turn turn) {
        switch (input) {
            case 0:
                return new HumanAgent(turn);

            case 1:
                return new PureMonteCarloAgent(turn);

            case 2:
                return new MonteCarloAgent(turn);

            default:
                throw new IllegalArgumentException();
        }
    }

}

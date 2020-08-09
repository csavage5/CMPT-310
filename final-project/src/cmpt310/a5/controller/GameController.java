package cmpt310.a5.controller;

import cmpt310.a5.model.*;
import cmpt310.a5.view.*;

/**
 * Receives user input and sends the Model commands based on that input.
 * Receives results from Model and tells the View what to display.
 */
public class GameController {

    private Game game;


    public GameController() {
        // TODO prompt user to choose which agents
        //  occupy which player slots

        Integer[] selection = TextOutput.selectPlayerPrompt();
        game = new Game(getAgentTypeFromInput(selection[0], Board.Turn.PLAYER1),
                getAgentTypeFromInput(selection[1], Board.Turn.PLAYER2));

        gameLoop();
    }

    private void gameLoop() {
        //System.out.println("nanosecond length: " + System.nanoTime());
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
            System.out.println("Game is over: both players could not place a tile.");
        } else if (game.board.isBoardFilled()) {
            System.out.println("Game is over: game board is filled.");
        }

        TextOutput.printGameOver(game.board.victor, game.board.getScoreP1(), game.board.getScoreP2());

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

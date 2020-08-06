package cmpt310.a5.controller;

import cmpt310.a5.model.*;
import cmpt310.a5.view.*;

import java.util.Scanner;

/**
 * Receives user input and sends the Model commands based on that input.
 * Receives results from Model and tells the View what to display.
 */
public class GameController {

    private Game game;
    public static final Scanner scanner = new Scanner(System.in);


    public GameController() {
        // TODO prompt user to choose which agents
        //  occupy which player slots
        game = new Game(new HumanAgent(Board.Turn.PLAYER1),
                new HumanAgent(Board.Turn.PLAYER2));

        gameLoop();
    }

    private void gameLoop() {
        game.board.discoverValidMoves();
        TextOutput.printBoard(game.board.getGameBoardWithValidMoves());
        game.board.selectValidMove(Position.convertLetterNumber("F4"));
        TextOutput.printBoard(game.board.getGameBoardWithValidMoves());
        game.board.discoverValidMoves();
        TextOutput.printBoard(game.board.getGameBoardWithValidMoves());

    }

    /**
     * Prompts user for coordinate
     * @return index of move
     */
    public static int promptUserForInput() {
        TextOutput.promptCoordinateEntry();
        return Position.convertLetterNumber(scanner.nextLine());
    }
}

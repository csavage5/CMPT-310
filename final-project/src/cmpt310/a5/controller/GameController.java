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

    public GameController() {
        // TODO prompt user to choose which agents
        //  occupy which player slots
        game = new Game(new MonteCarloAgent(Game.Turn.PLAYER1),
                new HumanAgent(Game.Turn.PLAYER2));


        gameLoop();
    }

    private void gameLoop() {

        Scanner scanner = new Scanner(System.in);
        game.board.discoverValidMoves(Board.Tile.Player1);
        TextOutput.printBoard(game.board.getGameBoardWithValidMoves());

    }
}

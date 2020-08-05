package cmpt310.a5.controller;

import cmpt310.a5.model.Game;
import cmpt310.a5.view.*;

import java.util.Scanner;


/**
 * Receives user input and sends the Model commands based on that input.
 * Receives results from Model and tells the View what to display.
 */
public class GameController {

    public GameController() {
        gameLoop();
    }

    private void gameLoop() {
        Game game = new Game();
        Scanner scanner = new Scanner(System.in);

        TextOutput.printBoard(game.getBoard());

    }
}

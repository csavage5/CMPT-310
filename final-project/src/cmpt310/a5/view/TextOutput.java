package cmpt310.a5.view;

import cmpt310.a5.controller.GameController;
import cmpt310.a5.model.*;

import java.util.ArrayList;
import java.util.Scanner;

/**
 * Pushes UI to console output
 */
public class TextOutput {

    public static final Scanner scanner = new Scanner(System.in);

    private static String topLetters = "    A   B   C   D   E   F   G   H";
    private static String sideNumbers = "12345678";
    private static String divider = "  ---------------------------------";

    private static String inputPrompt = "Enter a coordinate of a valid move (*): ";

    public static void printBoard(ArrayList<Board.Tile> gameBoard) {
        System.out.println(topLetters);
        System.out.println(divider);
        for (int y = 0; y < 8; y++) {

            for (int x = 0; x < 8; x++) {

                // ** side numbers ** //
                if (x == 0) {
                    System.out.print(sideNumbers.charAt(y));
                }

                // cell divider
                System.out.print(" | ");

                //TODO print game tile
                switch (gameBoard.get(Position.convertCartesian(x, y))) {

                    case Empty:
                        System.out.print(" ");
                        break;

                    case Player1:
                        System.out.print("X");
                        break;

                    case Player2:
                        System.out.print("O");
                        break;

                    case ValidMove:
                        System.out.print("*");
                        break;
                }


            }

            // end of line
            System.out.println(" |");
            System.out.println(divider);

        }

    }

    public static void printScores(int scoreP1, int scoreP2) {
        System.out.println("Score (P1, X): " + scoreP1 + "\nScore (P2, O): " + scoreP2);
    }

    public static void printTurnInformation(Board.Turn state, int scoreP1, int scoreP2) {
        printScores(scoreP1, scoreP2);
        switch (state) {
            case PLAYER1:
                System.out.println("Now Player 1's turn (X).");
                break;

            case PLAYER2:
                System.out.println("Now Player 2's turn (O).");
        }
    }

    public static void printSkippedTurn(Board.Turn skippedPlayer) {
        System.out.println(skippedPlayer.name() + "'s turn is skipped, has no valid moves.");
    }

    public static void printGameOver(Board.Turn victor, int scoreP1, int scoreP2) {
        System.out.println("Game is over! The winner is: " + victor.name());
        printScores(scoreP1, scoreP2);

    }

    public static String promptCoordinateEntry() {
        System.out.print(inputPrompt);
        return scanner.nextLine();
    }


    public static Integer[] selectPlayerPrompt() {
        Integer[] result = new Integer[2];
        Boolean validEntries = false;
        Float estimatedTotalRuntime = (2) * ( (float) GameController.MAX_GAME_LOOPS / 60 );
        System.out.println("Welome to Reversi!");

        System.out.println("\nChoose the players for the game. The game will automatically " +
                "restart with the selected players " + GameController.MAX_GAME_LOOPS + " times.");

        System.out.println("\nWith the current settings of " + GameController.MAX_GAME_LOOPS + " game loops and " +
                        Game.MCTS_SEARCH_MAX_PLAYOUTS + " playouts per turn" +
                ", this will take an \nestimated time of " + estimatedTotalRuntime + " hours to complete " +
                "if two Monte Carlo agents are selected.\n");

        System.out.print("Enter: \n   0 for Human \n   1 for Pure Monte Carlo \n   2 for Monte Carlo with heuristics\n");

        while (!validEntries) {

            try {
                System.out.print("Choice for Player 1: ");
                result[0] = Integer.parseInt(scanner.nextLine());

                System.out.print("Choice for Player 2: ");
                result[1] = Integer.parseInt(scanner.nextLine());

                if (result[0] < 0 || result[0] > 2 || result[1] < 0 || result[1] > 2) {
                    throw new NumberFormatException();
                }

            } catch (NumberFormatException e) {
                System.out.println("Error: Invalid selection, try again\n");
                continue;
            }

            validEntries = true;
        }

        return result;
    }



}

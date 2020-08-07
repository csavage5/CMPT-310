package cmpt310.a5.view;

import cmpt310.a5.model.*;

import java.sql.SQLOutput;
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

    public static void printTurnInformation(Board.Turn state, int scoreP1, int scoreP2) {
        System.out.println("Score (P1): " + scoreP1 + "\nScore (P2): " + scoreP2);

        switch (state) {
            case PLAYER1:
                System.out.println("Now Player 1's turn (X).");
                break;

            case PLAYER2:
                System.out.println("Now Player 2's turn (O).");
        }
    }

    public static String promptCoordinateEntry() {
        System.out.print(inputPrompt);
        return scanner.nextLine();
    }


    // TODO prompts for choosing players
    public static Integer[] selectPlayerPrompt() {
        Integer[] result = new Integer[2];
        Boolean validEntries = false;

        System.out.println("Choose the players for the game.");
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



    // TODO

}

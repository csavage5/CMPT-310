package cmpt310.a5.view;

import cmpt310.a5.model.*;
import java.util.ArrayList;

/**
 * Pushes UI to console output
 */
public class TextOutput {
    private static String topLetters = "    A   B   C   D   E   F   G   H";
    private static String sideNumbers = "12345678";
    private static String divider = "  ---------------------------------";

    private static String inputPrompt = "Enter a coordinate of a valid move: ";

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

    public static void promptCoordinateEntry() {
        System.out.print(inputPrompt);
    }

    // TODO prompts for choosing players
    // TODO

}

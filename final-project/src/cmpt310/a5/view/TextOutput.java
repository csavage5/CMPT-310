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

    //ArrayList<Board.Tile> board
    public static void printBoard() {
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
                System.out.print(" ");

            }

            // end of line
            System.out.println(" |");
            System.out.println(divider);

        }

    }

}

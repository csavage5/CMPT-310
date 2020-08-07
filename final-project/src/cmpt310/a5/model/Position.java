package cmpt310.a5.model;

import java.util.HashMap;

/**
 * Utility class
 */
public class Position {

    public static final int WIDTH = 8;
    public static final int HEIGHT = 8;

    private static HashMap<String, Integer> cols;

    static {
        cols = new HashMap<>();
        cols.put("A", 0);
        cols.put("B", 1);
        cols.put("C", 2);
        cols.put("D", 3);
        cols.put("E", 4);
        cols.put("F", 5);
        cols.put("G", 6);
        cols.put("H", 7);
    }


    //region Board positions

    public static Boolean insideBoard(int[] cartesian) {
        return (cartesian[0] >= 0 && cartesian[0] < 8
                && cartesian[1] >= 0 && cartesian[1] < 8);
    }

    public static int modifyCoordinateInDirection(Board.Direction dir, int index) {
        int[] newCoord = modifyCoordinateInDirerctionCart(dir, index);
        return convertCartesian(newCoord[0], newCoord[1]);
    }

    public static int[] modifyCoordinateInDirerctionCart(Board.Direction dir, int index) {
        int[] cartesian = convertIndex(index);
        switch (dir) {
            case Up:
                cartesian[1] -= 1;
                break;
            case Down:
                cartesian[1] += 1;
                break;
            case Left:
                cartesian[0] -= 1;
                break;
            case Right:
                cartesian[0] += 1;
                break;
            case DiagUpLeft:
                cartesian[0] -= 1;
                cartesian[1] -= 1;
                break;
            case DiagUpRight:
                cartesian[0] += 1;
                cartesian[1] -= 1;
                break;
            case DiagDownLeft:
                cartesian[0] -= 1;
                cartesian[1] += 1;
                break;
            case DiagDownRight:
                cartesian[0] += 1;
                cartesian[1] += 1;
                break;
            default:
                break;
        }

        return cartesian;

    }

    public static boolean willNotMoveOutsideOfBoard(Board.Direction dir, int index) {
        return (insideBoard(modifyCoordinateInDirerctionCart(dir, index)));
    }

    //endregion

    //region Converter utility methods
    /**
     * Convert Letter-Number format to array index.
     * @param coord Caller must verify this is in a
     *              valid format - i.e. "A2"
     * @return
     */
    public static int convertLetterNumber(String coord) {
        // Convert column letter to number
        int x = cols.get(coord.substring(0, 1).toUpperCase());
        int y = Integer.parseInt(coord.substring(1)) - 1;

        return (x + (y * WIDTH));
    }

    public static int convertCartesian(int x, int y) {
        return (x + (y * WIDTH));
    }

    public static int[] convertIndex(int index) {
        // will take floor of division
        int y = index / WIDTH;
        int x = index - (y * WIDTH);

        return new int[]{x, y};
    }

    //endregion


}

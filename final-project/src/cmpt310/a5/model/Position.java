package cmpt310.a5.model;

import java.util.HashMap;

/**
 * Utility class for coordinate conversion
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

    /**
     * Convert Letter-Number format to array index.
     * @param coord Caller must verify this is in a
     *              valid format - i.e. "A2"
     * @return
     */
    public static int convertLetterNumber(String coord) {
        // Convert column letter to number
        int x = cols.get(coord.substring(0, 1));
        int y = Integer.parseInt(coord.substring(1)) - 1;

        return (x + (y * WIDTH));
    }

    public static int convertCartesian(int x, int y) {
        return (x + (y * WIDTH));
    }



}

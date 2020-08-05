package cmpt310.a5.model;

import java.util.ArrayList;
import java.util.HashMap;

public class Board {

    public enum Tile {
        Player1,
        Player2,
        ValidMove,
        Empty
    }

    public enum Direction {
        Up,
        Down,
        Left,
        Right,
        DiagUpLeft,
        DiagUpRight,
        DiagDownLeft,
        DiagDownRight
    }

    private ArrayList<Tile> gameBoard;

    //(valid move index, originating tiles)
    private HashMap<Integer, ArrayList<Integer>> validMoves;

    private int scorePlayer1 = 2;
    private int scorePlayer2 = 2;

    public Board() {
        this.gameBoard = new ArrayList<Tile>(8 * 8);

        // fill board
        for (int i = 0; i < 64; i++) {
            gameBoard.add(Tile.Empty);
        }

        // System.out.println(gameBoard.size());
        gameBoard.set(Position.convertLetterNumber("D4"), Tile.Player1);
        gameBoard.set(Position.convertLetterNumber("E4"), Tile.Player2);
        gameBoard.set(Position.convertLetterNumber("E5"), Tile.Player1);
        gameBoard.set(Position.convertLetterNumber("D5"), Tile.Player2);
    }

    public ArrayList<Tile> getGameBoard() {
        return (ArrayList<Tile>) gameBoard.clone();
    }

    public int getScore(Tile player) {
        // TODO implement
        return 0;
    }

    /**
     * Discover and save valid moves in validMoves for the given
     * tile type
     * @param playerTile type of tile to generate valid moves from
     */
    public void discoverValidMoves(Tile playerTile) {

        Tile enemyTile;

        switch (playerTile) {
            case Player1:
                enemyTile = Tile.Player2;
                break;

            case Player2:
                enemyTile = Tile.Player1;
                break;
            default:
                throw new IllegalStateException("Unexpected value: " + playerTile);
        }

        // iterate through all tiles in gameBoard
        // that are owned by agent, discover valid
        // moves from that tile
        int index = 0;
        for ( Tile itr : gameBoard) {

            if (itr == playerTile) {

                int prevIndex = index;
                int currentIndex = index;

                // ** Check all directions for valid moves ** //
                for (Direction dir : Direction.values()) {

                    currentIndex = Position.modifyCoordinateInDirerction(dir, currentIndex);

                    // end when game borders are crossed
                    while (Position.insideBoard(Position.convertIndex(currentIndex))) {

                        if (gameBoard.get(currentIndex) == playerTile) {
                            // move on to next direction
                            break;
                        }

                        if (gameBoard.get(currentIndex) == Tile.Empty) {

                            if (gameBoard.get(prevIndex) == enemyTile) {
                                // add index as an originating tile for currentIndex
                                ArrayList<Integer> value = validMoves.getOrDefault(currentIndex, new ArrayList<>());
                                value.add(index);
                                validMoves.put(currentIndex, value);
                            }

                            // move on to next direction
                            break;

                        } else {
                            // pattern not yet found, increment other values
                            prevIndex = currentIndex;
                        }

                    }

                }

            }

            index += 1;
        }

    }


    public void selectValidMove(int validMovePosition) {
        // TODO implement

        // TODO check dictionary for originating tile(s)
        //  of valid move

        // TODO change tile alignment for tiles between
        //  valid tile and originating tile(s) to player
        //  with current turn

        // TODO adjust score for both players
    }

}

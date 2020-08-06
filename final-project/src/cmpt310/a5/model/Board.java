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

    private Enum<Game.Turn> state = Game.Turn.PLAYER1;

    private ArrayList<Tile> gameBoard;

    //(valid move index, originating tiles)
    private HashMap<Integer, ArrayList<Integer>> validMoves;

    private int scorePlayer1 = 2;
    private int scorePlayer2 = 2;

    public Board() {
        this.gameBoard = new ArrayList<Tile>(8 * 8);
        this.validMoves = new HashMap<>();
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

    //region Accessors

    public ArrayList<Tile> getGameBoard() {
        return (ArrayList<Tile>) gameBoard.clone();
    }

    public int getScore(Tile player) {
        // TODO implement
        return 0;
    }

    public ArrayList<Tile> getGameBoardWithValidMoves() {
        ArrayList<Tile> newGameBoard = getGameBoard();

        for (int key : validMoves.keySet()) {
            newGameBoard.set(key, Tile.ValidMove);
        }

        return newGameBoard;
    }

    //endregion

    /**
     * Discover and save valid moves in validMoves for the given
     * tile type
     * @param playerTile type of tile to generate valid moves from
     */
    public void discoverValidMoves(Tile playerTile) {
        // TODO break into separate methods

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
        ArrayList<Integer> pathToGoal = new ArrayList<>();
        for (Tile itr : gameBoard) {

            if (itr == playerTile) {

                int prevIndex = index;
                int currentIndex = index;

                // ** Check all directions for valid moves ** //
                for (Direction dir : Direction.values()) {
                    System.out.println("Moving in direction " + dir);
                    System.out.print("At index " + currentIndex + ", moving to ");

                    pathToGoal.clear();
                    currentIndex = Position.modifyCoordinateInDirerction(dir, currentIndex);
                    System.out.println(currentIndex);

                    // end when game borders are crossed
                    while (Position.insideBoard(Position.convertIndex(currentIndex))) {

                        pathToGoal.add(currentIndex);

                        // found own before an empty tile => end search in this direction
                        if (gameBoard.get(currentIndex) == playerTile) {
                            // move on to next direction
                            break;
                        }

                        // found empty tile
                        if (gameBoard.get(currentIndex) == Tile.Empty) {

                            if (gameBoard.get(prevIndex) == enemyTile) {
                                System.out.println("found valid move at " + currentIndex);

                                // add index as an originating tile for currentIndex
                                ArrayList<Integer> value = validMoves.getOrDefault(currentIndex, new ArrayList<>());
                                value.addAll(pathToGoal);
                                validMoves.put(currentIndex, value);
                            }

                            // move on to next direction
                            break;

                        } else {
                            // pattern not yet found, increment other values
                            prevIndex = currentIndex;
                            currentIndex = Position.modifyCoordinateInDirerction(dir, currentIndex);
                        }

                    }

                    // reset index
                    prevIndex = index;
                    currentIndex = index;

                }

            }

            index += 1;
        }

    }

    public void selectValidMove(int validMovePosition) {

        // check for existence of valid move at given position
        if (!validMoves.containsKey(validMovePosition)) {
            throw new IllegalArgumentException("Selected move is invalid");
        }

        // check dictionary for list of tiles to flip
        ArrayList<Integer> tilesToFlip = validMoves.get(validMovePosition);

        // change tile alignment for tiles on path -
        //  *should* be # of elements in list
        for (Integer itr : tilesToFlip) {
            changeTileAlignment(itr);
        }

    }

    private void changeTileAlignment(int index) {

        Tile tileToFlip = gameBoard.get(index);

        // TODO adjust score for both players
        //  - reduce and add for every flipped tile,
        //  only add for placing a new tile
        //  ** Need to know turn for this

        switch (tileToFlip) {
            case Player1:
                gameBoard.set(index, Tile.Player2);
                scorePlayer2++;
                scorePlayer1--;
                break;

            case Player2:
                gameBoard.set(index, Tile.Player1);
                scorePlayer1++;
                scorePlayer2--;
                break;

            case ValidMove:

                if (state == Game.Turn.PLAYER1) {
                    gameBoard.set(index, Tile.Player1);
                    scorePlayer1++;
                } else {
                    gameBoard.set(index, Tile.Player2);
                    scorePlayer2++;
                }

                System.out.println("placing tile at valid move " + index);
                break;

            case Empty:
                // FIXME valid moves not saved to board, so
                //  tile type ValidMove not found
                System.out.println("cannot flip tile at " + index);
                return;
        }


    }

}

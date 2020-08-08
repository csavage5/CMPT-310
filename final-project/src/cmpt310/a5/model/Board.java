package cmpt310.a5.model;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class Board {

    //region Enums
    public enum Turn {
        PLAYER1(0),
        PLAYER2(1),
        NONE(2),
        TIE(3);

        private int value;
        private boolean didSkip;

        Turn(int value) {
            this.value = value;
        }

        public boolean isDidSkip() {
            return didSkip;
        }

        public Turn getOpposite() {
            switch (this.value) {
                case 0:
                    return PLAYER2;
                case 1:
                    return PLAYER1;
                default:
                    return NONE;
            }
        }

    }

    public enum Tile {
        Player1(0),
        Player2(1),
        ValidMove(2),
        Empty(3);

        private int value;

        Tile(int value) {
            this.value = value;
        }
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
    //endregion

    public Turn state = Turn.PLAYER1;
    public Turn victor = Turn.NONE;

    private ArrayList<Tile> gameBoard;

    // (key, value) = (valid move index, path to originating tile)
    private HashMap<Integer, ArrayList<Integer>> validMoves;

    private int[] score = new int[]{2, 2};
    private boolean[] didSkipTurn = new boolean[]{false, false};

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

    public ArrayList<Tile> getGameBoardWithValidMoves() {
        ArrayList<Tile> newGameBoard = getGameBoard();

        for (int key : validMoves.keySet()) {
            newGameBoard.set(key, Tile.ValidMove);
        }

        return newGameBoard;
    }

    public int getScore(Turn player) {
        return score[state.value];
    }

    public int getScoreP1(){
        return score[Turn.PLAYER1.value];
    }

    public int getScoreP2() {
        return score[Turn.PLAYER2.value];
    }

    public int getStateValue() {
        return state.value;
    }

    //endregion



    //region State maintenance

    private void increaseScore(Turn player) {
        score[player.value] += 1;
    }

    private void decreaseScore(Turn player) {
        score[player.value] -= 1;
    }

    private boolean isBoardFilled() {
        return (getScore(state) + getScore(state.getOpposite()) > 63);
    }

    private boolean didBothPlayersSkip() {
        return (didSkipTurn[state.value] && didSkipTurn[state.value]);
    }

    private void checkForVictor() {
        if (checkEndConditions()) {
            // set victor to player with higher score
            if (getScoreP1() > getScoreP2()){
                victor = Turn.PLAYER1;
            } else if (getScoreP1() < getScoreP2()) {
                victor = Turn.PLAYER2;
            } else {
                victor = Turn.TIE;
            }
        }
    }

    private boolean checkEndConditions() {
        return (isBoardFilled() || didBothPlayersSkip());
    }

    public boolean isGameOver() {
        return (victor != Turn.NONE);
    }

    public void switchTurn() {
        didSkipTurn[state.value] = false;
        state = state.getOpposite();
    }

    private void skipTurn() {
        didSkipTurn[state.value] = true;
        state = state.getOpposite();
    }

    //endregion



    //region Gameplay
    /**
     * Discover and save valid moves in validMoves. Uses state to determine
     * the turn of the current player
     * @return true if at least 1 valid move was discovered
     */
    public boolean discoverValidMoves() {
        // TODO break into separate methods
        Tile playerTile = null;
        Tile enemyTile = null;

        switch (state) {
            case PLAYER1:
                playerTile = Tile.Player1;
                enemyTile = Tile.Player2;
                break;

            case PLAYER2:
                playerTile = Tile.Player2;
                enemyTile = Tile.Player1;
                break;

            default:
                throw new IllegalStateException("'state' was not set to a player");
        }

        // iterate through all tiles in gameBoard
        // that are owned by agent, discover valid
        // moves from that tile
        int index = 0;
        validMoves.clear();

        for (Tile itr : gameBoard) {

            if (itr == playerTile) {
                // ** Check all directions for valid moves ** //
                for (Direction dir : Direction.values()) {
                    getValidMoveInDirection(dir, index, playerTile, enemyTile);
                    //System.out.println("Moving in direction " + dir);
                    //System.out.print("At index " + currentIndex + ", moving to ");
                }
            }

            index += 1;
        }

        if (validMoves.keySet().size() == 0) {
            //no valid moves found, skip turn
            skipTurn();
            return false;
        }

        return true;
    }

    private void getValidMoveInDirection(Direction dir, int startingIndex, Tile playerTile, Tile enemyTile) {
        int prevIndex = startingIndex;
        int currentIndex = startingIndex;

        ArrayList<Integer> pathToGoal = new ArrayList<>();
        boolean foundGoal = false;

        // check if next move will go outside of the board
        while (Position.willNotMoveOutsideOfBoard(dir, currentIndex) && !foundGoal) {
            currentIndex = Position.modifyCoordinateInDirection(dir, currentIndex);
            pathToGoal.add(currentIndex);

            // found own tile before an empty tile => end search in this direction
            if (gameBoard.get(currentIndex) == playerTile) {
                // move on to next direction
                foundGoal = true;

            } else if (gameBoard.get(currentIndex) == Tile.Empty) {
                // found empty tile

                if (gameBoard.get(prevIndex) == enemyTile) {
                    //System.out.println("found valid move at " + currentIndex);

                    // add index as an originating tile for currentIndex
                    ArrayList<Integer> value = validMoves.getOrDefault(currentIndex, new ArrayList<>());
                    value.addAll(pathToGoal);
                    validMoves.put(currentIndex, value);
                }

                // found move, stop searching
                foundGoal = true;

            } else {
                // pattern not yet found, increment other values
                prevIndex = currentIndex;
            }

        }



    }

    public void selectValidMove(int validMovePosition) {
        Integer[] flippedTiles = generateNewBitmap();

        // check for existence of valid move at given position
        if (!validMoves.containsKey(validMovePosition)) {
            throw new IllegalArgumentException("Selected move is invalid");
        }

        // check dictionary for list of tiles to flip
        ArrayList<Integer> tilesToFlip = validMoves.get(validMovePosition);

        // change tile alignment for tiles on path -
        //  *should* be # of elements in list
        for (Integer itr : tilesToFlip) {
            if (flippedTiles[itr] == 0) {
                changeTileAlignment(itr);
                flippedTiles[itr] = 1;
            }
        }

        //check if game is won
        checkForVictor();

        if (isGameOver()) {
            return;
        }

        switchTurn();

    }

    private void changeTileAlignment(int index) {

        Tile tileToFlip = getGameBoardWithValidMoves().get(index);


        switch (tileToFlip) {
            case Player1:
                gameBoard.set(index, Tile.Player2);
                increaseScore(Turn.PLAYER2);
                decreaseScore(Turn.PLAYER1);
                break;

            case Player2:
                gameBoard.set(index, Tile.Player1);
                increaseScore(Turn.PLAYER1);
                decreaseScore(Turn.PLAYER2);
                break;

            case ValidMove:

                if (state == Turn.PLAYER1) {
                    gameBoard.set(index, Tile.Player1);
                    increaseScore(Turn.PLAYER1);
                } else {
                    gameBoard.set(index, Tile.Player2);
                    increaseScore(Turn.PLAYER2);
                }

                System.out.println("placing tile" + state + " at valid move " + index);
                validMoves.clear();
                break;

            case Empty:
                System.out.println("cannot flip empty tile at " + index);
                return;
        }


    }

    //endregion



    //region Utility

    private Integer[] generateNewBitmap() {
        Integer[] array = new Integer[64];
        Arrays.fill(array, 0);
        return array;
    }


    //endregion


}

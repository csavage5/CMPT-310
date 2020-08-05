package cmpt310.a5.model;

import java.util.ArrayList;
import java.util.Collections;

public class Board {

    public enum Tile {
        Player1,
        Player2,
        ValidMove,
        Empty
    }

    private ArrayList<Tile> gameBoard;

    public Board() {
        this.gameBoard = new ArrayList<Tile>(8 * 8);

        // fill board
        for (int i = 0; i < 64; i++) {
            gameBoard.add(Tile.Empty);
        }

        System.out.println(gameBoard.size());
        gameBoard.set(Position.convertLetterNumber("D4"), Tile.Player1);
        gameBoard.set(Position.convertLetterNumber("E4"), Tile.Player2);
        gameBoard.set(Position.convertLetterNumber("E5"), Tile.Player1);
        gameBoard.set(Position.convertLetterNumber("D5"), Tile.Player2);
    }

    public ArrayList<Tile> getGameBoard() {
        return gameBoard;
    }

    public int getScore(Tile player) {
        // TODO implement
        return 0;
    }
}

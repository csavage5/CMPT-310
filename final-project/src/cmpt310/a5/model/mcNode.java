package cmpt310.a5.model;

import cmpt310.a5.view.TextOutput;
import jdk.jshell.spi.ExecutionControl;

import java.util.ArrayList;
import java.util.Random;
import java.util.Set;

public class mcNode {

    protected ArrayList<mcNode> children = new ArrayList<>();
    public mcNode parent;
    public Board board;
    public int validMoveLocation;
    public boolean leafNode = false;
    protected Random rand = new Random();

    protected int evalMetric;
    protected int wins;
    protected int losses;
    protected int draws;
    protected int simulations;

    public mcNode(Board board) {
        this.board = board;
        this.parent = null;
    }

    public mcNode(mcNode parent, Board board) {
        this.parent = parent;
        this.board = board;

        //generateChildren();
    }

    public void generateChildren() {
        if (children.size() > 0) {
            return;
        }
        System.out.println("in generateChildren()...");
        board.discoverValidMoves();
        mcNode temp;
        ArrayList<Integer> keys = new ArrayList<>(board.validMoves.keySet());
        for (Integer key : keys) {
            // generate new node, add cloned board + current node as parent
            try {
                temp = new mcNode(this, (Board) board.clone());

                // make a valid move
                temp.board.selectValidMove(key);
                validMoveLocation = key;
                children.add(temp);
                System.out.println("gameboard after adding a child:");
                TextOutput.printBoard(board.getGameBoardWithValidMoves());

            } catch (CloneNotSupportedException e) {
                System.out.println("Error: failed to clone board to new mcNode");
                e.printStackTrace();
            }

        }

        if (children.size() == 0) {
            System.out.println("hit leaf node");
            leafNode = true;
        }

    }

    public mcNode getRandomChild() {
        if (children.size() == 0) {
            throw new IllegalStateException("Trying to generate children of a leaf node");
        }

        return children.get(rand.nextInt(children.size()));
    }

    public void updateEvalMetric() {
        evalMetric = wins + draws - losses;
    }

    public mcNode getBestChild() {
        mcNode bestChild = children.get(0);

        for (mcNode itr : children) {
            if (itr.evalMetric > bestChild.evalMetric) {
                bestChild = itr;
            }
        }

        return bestChild;
    }


    //region Statistics

    public void increaseWins() {
        wins++;
        updateEvalMetric();
    }

    public void increaseLosses() {
        losses++;
        updateEvalMetric();
    }

    public void increaseDraws() {
        draws++;
        updateEvalMetric();
    }

    public void increaseSims() {
        simulations++;
    }

    //endregion

    public void displayChildInfo() {
        String info = "";
        int index = 0;
        for (mcNode child : children) {
            info += "Option #" + index + "\n" + "   " +
                    "move coord: " + validMoveLocation + "\n" + "   " +
                    "wins: " + wins + "\n" + "   " +
                    "losses: " + losses  + "\n" + "   " +
                    "draws: "  + "\n" + "   " +
                    "eval metric: " + evalMetric + "\n\n";
        }
        System.out.println(info);
    }
}

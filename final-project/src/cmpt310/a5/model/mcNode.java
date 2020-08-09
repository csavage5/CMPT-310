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

        if (board.isGameOver()) {
            leafNode = true;
            return;
        }

        System.out.print("Generating children...");

        if (board.discoverValidMoves()) {
            System.out.println(board.validMoves.keySet());
            mcNode temp;
            for (Integer key : board.validMoves.keySet()) {
                // generate new node, add cloned board + current node as parent
                temp = new mcNode(this, board.cloneBoard());

                // make a valid move
                temp.board.selectValidMove(key);
                temp.validMoveLocation = key;
                children.add(temp);
                //System.out.println("gameboard after adding a child:");
                //TextOutput.printBoard(board.getGameBoardWithValidMoves());
            }

        } else {

            // this turn is skipped and game is still valid
            // add current board as sole child of this state
            children.add(new mcNode(this, board.cloneBoard()));
        }

        System.out.print("Done.");


    }

    public mcNode getRandomChild() {
        System.out.println("children size: " + children.size());
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

            index += 1;
        }
        System.out.println(info);
    }
}

package cmpt310.a5.model;

import java.util.ArrayList;
import java.util.Random;


/**
 * Facilitates the tree structure of pure MCTS
 */
public class mcNode {

    protected ArrayList<mcNode> children = new ArrayList<>();
    public mcNode parent;
    public Board board;
    public int validMoveLocation;
    public boolean leafNode = false;
    protected Random rand = new Random();

    protected Double evalMetric = 0.0;
    protected long wins = 0;
    protected long losses = 0;
    protected long draws = 0;
    protected long visits = 0;

    public mcNode(Board board) {
        this.board = board;
        this.parent = null;
    }

    public mcNode(mcNode parent, Board board) {
        this.parent = parent;
        this.board = board;

    }

    public void generateChildren() {
        if (children.size() > 0) {
            return;
        }

        if (board.isGameOver()) {
            leafNode = true;
            return;
        }

        if (board.discoverValidMoves()) {

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

    }

    /**
     * Chooses a child of the current node to explore next.
     * For Pure MCTS, this is done randomly.
     * @return node to explore next
     */
    public mcNode getChildToExplore() {
        //System.out.println("children size: " + children.size());
        if (children.size() == 0) {
            throw new IllegalStateException("Trying to generate children of a leaf node");
        }

        return children.get(rand.nextInt(children.size()));
    }

    public void updateEvalMetric() {
        evalMetric = (double) (wins + draws) / losses;
    }

    public mcNode getBestChild() {
        mcNode bestChild = children.get(0);
        int index = 0;
        int bestIndex = 0;
        for (mcNode itr : children) {
            if (itr.evalMetric > bestChild.evalMetric) {
                bestChild = itr;
                bestIndex = index;
            }
            index += 1;

        }
        System.out.println("Chose Option #" + bestIndex + " (" +
                Position.convertIndexToLetterNumber(bestChild.validMoveLocation) + ").\n");
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
        visits++;
    }

    //endregion

    public void displayChildInfo() {
        String info = "";
        int index = 0;
        for (mcNode child : children) {
            info += "Option #" + index + "\n" + "   " +
                    "coordinate: " + Position.convertIndexToLetterNumber(child.validMoveLocation) + "\n" + "   " +
                    "wins: " + child.wins + "\n" + "   " +
                    "losses: " + child.losses  + "\n" + "   " +
                    "draws: "  + child.draws + "\n" + "   " +
                    "total playouts: " + child.visits + "\n" + "   " +
                    "eval metric: " + child.evalMetric + "\n";

            index += 1;
        }
        System.out.println(info);
    }
}

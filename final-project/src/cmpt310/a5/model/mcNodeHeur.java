package cmpt310.a5.model;

import java.lang.Math;
import java.util.*;

/**
 * Duplicate of McNode, but has overloaded functions to
 * search for nodes with a heuristic instead of randomly
 */

//TODO see if this can be subclassed to mcNode again

public class mcNodeHeur {
    protected ArrayList<mcNodeHeur> children = new ArrayList<>();
    public mcNodeHeur parent;
    public Board board;
    public int validMoveLocation;
    public boolean leafNode = false;
    protected Random rand = new Random();
    int bestChildIndex = 0;

    // Statistics
    protected long wins = 0;
    protected long losses = 0;
    protected long draws = 0;
    protected long visits = 0;

    // for UCT calculation
    protected Double evalMetric = 0.0;
    public float uctScaleCorners = 1;
    public float uctScaleMobilityActualOpposing = 1;
    public float uctScaleMobilityPotential = 1;
    protected double exploitation;
    protected double exploration;
    protected double c = Math.sqrt(2);

    // Heuristics

    // corners are good positions
    private final List<Integer> goodPositionCorner = Arrays.asList(0, 7, 50, 63);

    // positions left/right/up/down from corners are bad
    private final List<Integer> badPositionCornerAdjCardinal =
            Arrays.asList(1, 8, 6, 15, 48, 57, 55, 62);

    // positions at diagonals from corners are very bad
    private final List<Integer> veryBadPositionCornerAdjDiag =
            Arrays.asList(9, 14, 49, 54);


    private Board.Turn agentOrder;
    private boolean isRoot = false;


    //region Constructors
    public mcNodeHeur(Board board) {
        this.board = board;
        this.parent = null;
        agentOrder = board.state;
        isRoot = true;
    }

    public mcNodeHeur(mcNodeHeur parent, Board board, Board.Turn agentOrder) {
        this.parent = parent;
        this.board = board;
        this.agentOrder = agentOrder;

        // update eval parameter
        //this.increaseVisits();
        this.updateEvalMetric();
    }

    //endregion


    public void generateOrUpdateChildren() {
        increaseVisits();

        if (children.size() > 0) {
            // children already generated - need to update
            // their evals to reflect increased visit count
            // of parent
            for (mcNodeHeur child : children) {
                child.updateEvalMetric();
            }

            return;
        }

        if (board.isGameOver()) {
            leafNode = true;
            return;
        }

        //System.out.print("Generating children...");

        if (board.discoverValidMoves()) {
            //System.out.println(board.validMoves.keySet());
            mcNodeHeur temp;
            for (Integer key : board.validMoves.keySet()) {
                // generate new node, add cloned board + current node as parent
                temp = new mcNodeHeur(this, board.cloneBoard(), agentOrder);

                checkHeuristicsPreMove(key, temp);

                // make a valid move
                temp.board.selectValidMove(key);
                temp.validMoveLocation = key;

                checkHeuristicsPostMove(temp);
                temp.updateEvalMetric();

                children.add(temp);
                //System.out.println("gameboard after adding a child:");
                //TextOutput.printBoard(board.getGameBoardWithValidMoves());
            }

        } else {

            // this turn is skipped and game is still valid
            // add current board as sole child of this state
            children.add(new mcNodeHeur(this, board.cloneBoard(), agentOrder));
        }

        //System.out.print("Done.");


    }

    /**
     * Chooses a child of the current node to explore next.
     * For non-pure MCTS, this is done by picking the best
     * child node based on evaluation criteria.
     * @return node to explore next
     */
    public mcNodeHeur getChildToExplore() {
        //System.out.println("children size: " + children.size());
        if (children.size() == 0) {
            throw new IllegalStateException("Trying to generate children of a leaf node");
        }

        // choose child based on eval criteria
        //Collections.shuffle(children);
        mcNodeHeur bestChild = children.get(0);
        int index = 0;

        for (mcNodeHeur itr : children) {
            if (itr.evalMetric > bestChild.evalMetric) {
                bestChild = itr;
                bestChildIndex = index;
            }
            index += 1;
        }


        return bestChild;

    }

    public mcNodeHeur getBestChild() {
        mcNodeHeur bestChild = getChildToExplore();

        System.out.println("Chose Option #" + bestChildIndex + " (" +
                Position.convertIndexToLetterNumber(bestChild.validMoveLocation) + ").\n");
        return bestChild;
    }

    /**
     * Called *before* the child makes the valid move. This method evaluates the valid move
     * via heuristics and adjusts the uctScaleFactor in the child
     * @param move
     * @param newNode
     */
    public void checkHeuristicsPreMove(int move, mcNodeHeur newNode) {
        //float val = 1f;

        // check for corners

        // set val according to which player's turn it is
        // i.e. if it's this agent's turn, the corner move will
        //      increase the uctScaleFactor, and the adjacent corner
        //      move will decrease it.

        // agent's turn
//        if (newNode.board.state == newNode.agentOrder) {
//            val = 1f;
//
//        } else if (newNode.board.state == newNode.agentOrder.getOpposite()) {
//            //not agent's turn
//            val = -1f;
//        }

        //TODO add documentation

        // Corner Heuristic Calculation
        if (goodPositionCorner.contains(move)) {
            // move in the corner - good move
            newNode.uctScaleCorners = (1.5f);
        } else if (badPositionCornerAdjCardinal.contains(move)) {
            // move adjacent to corner
            newNode.uctScaleCorners = (-0.5f);
        } else if (veryBadPositionCornerAdjDiag.contains(move)) {
            // move diagonal from corner
            newNode.uctScaleCorners = (-3.0f);
        }
    }

    private void checkHeuristicsPostMove(mcNodeHeur newNode) {
        // Mobility (Actual)

        //  Actual Mobility will measure the number of moves that the
        //  player for this board has. The smaller this value is, the better -
        //  goal is to minimize the number of possible moves for the opposing
        //  player. The reciprocal of this value is taken so that a smaller value
        //  will lead to a larger scale factor.
        if (newNode.board.discoverValidMoves()) {
            newNode.uctScaleMobilityActualOpposing = (1.0f / newNode.board.validMoves.size()) * 5;
        }

    }

    public void updateEvalMetric() {

        // UCT formula - from Wikipedia:
        // https://en.wikipedia.org/wiki/Monte_Carlo_tree_search#Exploration_and_exploitation

        exploitation = ( (double) wins + draws ) / (visits + 1);
        //System.out.println(Math.log(parent.visits));
        exploration = c * ( Math.sqrt( Math.log(parent.visits) / (visits + 1) ) );
        //System.out.println(exploration);
        evalMetric = exploitation + exploration;


        // Multiply evalMetric against the scale factor to get consistency if the
        // heuristic is not changed - i.e. if it stays at 1
        evalMetric = evalMetric +
                (evalMetric * uctScaleCorners) +
                (evalMetric * uctScaleMobilityActualOpposing);
    }


    //region Statistics

    public void increaseWins() {
        wins++;
        if (!isRoot) {
            parent.increaseWins();
            updateEvalMetric();
        }

    }

    public void increaseLosses() {
        losses++;
        if (!isRoot) {
            parent.increaseLosses();
            updateEvalMetric();
        }

    }

    public void increaseDraws() {
        draws++;
        if (!isRoot) {
            parent.increaseDraws();
            updateEvalMetric();
        }

    }

    public void increaseVisits() {
        visits++;
    }

    //endregion

    public void displayChildInfo() {
        String info = "";
        int index = 0;
        for (mcNodeHeur child : children) {
            info += "Option #" + index + "\n" + "   " +
                    "coordinate: " + Position.convertIndexToLetterNumber(child.validMoveLocation) + "\n" + "   " +
                    "wins: " + child.wins + "\n" + "   " +
                    "losses: " + child.losses  + "\n" + "   " +
                    "draws: "  + child.draws + "\n" + "   " +
                    "total playouts: " + child.visits + "\n" + "   " +
                    "eval metric: " + child.evalMetric + "\n" + "   " +
                    "eval heur. corners: " + child.uctScaleCorners + "\n" + "   " +
                    "eval heur. act. mobility: " + child.uctScaleMobilityActualOpposing + "\n" + "   " +
                    "exploitation: " + child.exploitation + "\n" + "   " +
                    "exploration: " + child.exploration + "\n";

            index += 1;
        }
        System.out.println(info);
    }


}

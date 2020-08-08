package cmpt310.a5.model;

import java.util.Random;


public class PureMonteCarloAgent extends Agent{

    private mcNode rootMcNode;
    private Random rand = new Random();

    public PureMonteCarloAgent(Board.Turn playerNumber) {
        super(playerNumber);
    }

    @Override
    public int makeMove(Board board) {
        // TODO implement

        // copy given board to starting node
        try {
            rootMcNode = new mcNode((Board) board.clone());
            rootMcNode.generateChildren();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }


        return pureMonteCarloSearch();
    }

    private int pureMonteCarloSearch() {

        mcNode cursor = rootMcNode;

        long startTime = System.currentTimeMillis();

        // run simulated playouts for 5 seconds
        while(System.currentTimeMillis() - startTime < 6000) {

            // randomly choose first child and
            // traverse tree from chosen child
            treeTraversal(rootMcNode.getRandomChild());

        }

        return rootMcNode.getBestChild().validMoveLocation;
    }

    private void treeTraversal(mcNode child) {
        mcNode cursor = child;

        while (!cursor.leafNode) {
            // randomly choose child
            cursor.generateChildren();
            cursor = child.getRandomChild();
        }

        // add to original child's win/loss/draw statistics
        // depending on victor value and this.playerNumber
        if (cursor.board.victor == this.playerNumber) {
            child.increaseWins();
        } else if (cursor.board.victor.getOpposite() == this.playerNumber) {
            child.increaseLosses();
        } else {
            child.increaseDraws();
        }

    }
}

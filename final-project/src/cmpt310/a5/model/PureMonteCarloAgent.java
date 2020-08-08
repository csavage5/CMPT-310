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
        System.out.println("Duplicating board to create root...");
        // copy given board to starting node

        rootMcNode = new mcNode(board.cloneBoard());
        rootMcNode.generateChildren();

        System.out.println("starting Pure MCTS...");
        return pureMonteCarloSearch();
    }

    private int pureMonteCarloSearch() {

        //mcNode cursor = rootMcNode;

        long startTime = System.currentTimeMillis();

        // run simulated playouts for 5 seconds
        while(System.currentTimeMillis() - startTime < 6000) {
            // randomly choose first child and
            // traverse tree from chosen child
            System.out.println("at root node");
            System.out.println("size of root's children: " + rootMcNode.children.size());
            treeTraversal(rootMcNode.getRandomChild());
        }

        rootMcNode.displayChildInfo();
        return rootMcNode.getBestChild().validMoveLocation;
    }

    private void treeTraversal(mcNode child) {
        System.out.println("at child of root node");
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

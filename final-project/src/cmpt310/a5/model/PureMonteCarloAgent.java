package cmpt310.a5.model;

import java.util.Random;


public class PureMonteCarloAgent extends Agent{

    private mcNode rootMcNode;
    private Random rand = new Random();
    private long totalIterations = 0;

    public PureMonteCarloAgent(Board.Turn playerNumber) {
        super(playerNumber);
    }

    @Override
    public int makeMove(Board board) {
        //System.out.println("Duplicating board to create root...");
        // copy given board to starting node
        totalIterations = 0;
        rootMcNode = new mcNode(board.cloneBoard());
        rootMcNode.generateChildren();

        System.out.println(playerNumber.name() + " is calculating (randomized)...");
        return pureMonteCarloSearch();
    }

    private int pureMonteCarloSearch() {

        //mcNode cursor = rootMcNode;

        //long startTime = System.currentTimeMillis();

        // run simulated playouts for Game.MCTS_SEARCH_TIME
        while(rootMcNode.visits < Game.MCTS_SEARCH_MAX_PLAYOUTS) {
            //System.out.println("current time: " + (System.currentTimeMillis() - startTime));
            // randomly choose first child and
            // traverse tree from chosen child
            //System.out.println("at root node");
            //System.out.println("size of root's children: " + rootMcNode.children.size());
            treeTraversal(rootMcNode.getChildToExplore());
            rootMcNode.visits++;
        }
        System.out.println("...done calculating.");
        rootMcNode.displayChildInfo();
        System.out.println("Total playouts: " + rootMcNode.visits);
        System.out.println("Total iterations: " + totalIterations);
        return rootMcNode.getBestChild().validMoveLocation;
    }

    private void treeTraversal(mcNode child) {
        //System.out.println("at child of root node");
        mcNode cursor = child;
        cursor.generateChildren();

        while (!cursor.board.isGameOver()) {
            // randomly choose child
            //System.out.println(cursor.board.isGameOver());
            totalIterations += 1;
            cursor = cursor.getChildToExplore();
            cursor.generateChildren();
        }

        child.increaseSims();

        // add to original child's win/loss/draw statistics
        // depending on victor value and this.playerNumber
        if (cursor.board.victor == this.playerNumber) {
            child.increaseWins();
            //System.out.println("Sim WIN");

        } else if (cursor.board.victor.getOpposite() == this.playerNumber) {
            child.increaseLosses();
            //System.out.println("Sim LOSS");

        } else {
            child.increaseDraws();
            //System.out.println("Sim DRAW");
        }

    }
}

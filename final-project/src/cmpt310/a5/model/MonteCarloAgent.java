package cmpt310.a5.model;


public class MonteCarloAgent extends Agent{

    private mcNodeHeur rootMcNode;

    public MonteCarloAgent(Board.Turn playerNumber) {
        super(playerNumber);
    }

    @Override
    public int makeMove(Board board) {
        //System.out.println("Duplicating board to create root...");
        // copy given board to starting node

        rootMcNode = new mcNodeHeur(board.cloneBoard());
        rootMcNode.generateOrUpdateChildren();
        //rootMcNode.displayChildInfo();

        System.out.println(playerNumber.name() + " is calculating...");
        return monteCarloSearch();
    }

    private int monteCarloSearch() {
        long startTime = System.currentTimeMillis();

        // run simulated playouts for 6 seconds
        while(System.currentTimeMillis() - startTime < 6000) {
            //System.out.println("current time: " + (System.currentTimeMillis() - startTime));
            // randomly choose first child and
            // traverse tree from chosen child
            //System.out.println("at root node");
            //System.out.println("size of root's children: " + rootMcNode.children.size());
            treeTraversal(rootMcNode.getChildToExplore());
            rootMcNode.generateOrUpdateChildren();
        }
        System.out.println("...done calculating.");
        rootMcNode.displayChildInfo();
        System.out.println("Total playouts: " + rootMcNode.visits);
        System.out.println("Total wins: " + rootMcNode.wins);
        return rootMcNode.getBestChild().validMoveLocation;
    }

    private void treeTraversal(mcNodeHeur child) {

        mcNodeHeur cursor = child;
        cursor.generateOrUpdateChildren();

        while (!cursor.board.isGameOver()) {
            // randomly choose child
            //System.out.println(cursor.board.isGameOver());
            cursor = cursor.getChildToExplore();
            cursor.generateOrUpdateChildren();
        }

        //System.out.println("Went " + counter + " levels deep to find endgame");
        // add to original child's win/loss/draw statistics
        // depending on victor value and this.playerNumber
        if (cursor.board.victor == this.playerNumber) {
            child.increaseWins();
            //System.out.println("Victory gameboard: ");
            //TextOutput.printBoard(cursor.board.getGameBoardWithValidMoves());
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

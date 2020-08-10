package cmpt310.a5.model;

import java.lang.Math;

/**
 * Duplicate of McNode, but has overloaded functions to
 * search for nodes with a heuristic instead of randomly
 */
public class mcNodeHeur extends mcNode{

    public mcNodeHeur(Board board) {
        super(board);
    }

    public mcNodeHeur(mcNode parent, Board board) {
        super(parent, board);
    }

    @Override
    public void generateChildren() {
        if (children.size() > 0) {
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
                temp = new mcNodeHeur(this, board.cloneBoard());

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
            children.add(new mcNodeHeur(this, board.cloneBoard()));
        }

        //System.out.print("Done.");


    }

    @Override
    public mcNode getNextChild() {
        //System.out.println("children size: " + children.size());
        if (children.size() == 0) {
            throw new IllegalStateException("Trying to generate children of a leaf node");
        }

        // choose child based on eval criteria
        mcNode bestChild = children.get(0);
        for (mcNode itr : children) {
            if (itr.evalMetric > bestChild.evalMetric) {
                bestChild = itr;
            }
        }

        return bestChild;

    }

    @Override
    public void updateEvalMetric() {
        // todo deal with children that haven't been explored,
        //  will have 0 wins / draws / losses
        double interior = (Math.log(parent.simulations) / simulations );
        evalMetric =  ((double) wins / simulations)  + ( Math.sqrt(2) * Math.sqrt(interior));
    }


    //region Statistics

    public void increaseWins() {
        wins++;
        parent.increaseWins();
        updateEvalMetric();
    }

    public void increaseLosses() {
        losses++;
        parent.losses++;
        updateEvalMetric();
    }

    public void increaseDraws() {
        draws++;
        parent.increaseDraws();
        updateEvalMetric();
    }

    public void increaseSims() {
        simulations++;
        //parent.increaseSims();
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
                    "total playouts: " + child.simulations + "\n" + "   " +
                    "eval metric: " + child.evalMetric + "\n";

            index += 1;
        }
        System.out.println(info);
    }


}

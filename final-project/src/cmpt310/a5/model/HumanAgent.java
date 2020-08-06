package cmpt310.a5.model;

import cmpt310.a5.controller.GameController;

public class HumanAgent extends Agent {

    public HumanAgent(Board.Turn playerNumber) {
        super(playerNumber);
    }

    @Override
    public int makeMove(Board board) {
        return GameController.promptUserForInput();
    }


}

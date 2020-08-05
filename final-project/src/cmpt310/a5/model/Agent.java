package cmpt310.a5.model;

public abstract class Agent {

    private Game.Turn playerNumber;

    public Agent(Game.Turn playerNumber) {
        this.playerNumber = playerNumber;
    }

    public abstract void makeMove();


}

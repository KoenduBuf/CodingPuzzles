import java.util.*;
import java.io.*;
import java.math.*;
import java.util.stream.Collectors;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Player {
    private static int size;
    private static int unitsPerPlayer;
    private static char[][] field;
    private static int legalActions;
    private static ActionList validActions;
    private static List<Unit> myUnits;
    private static List<Unit> enemyUnits;
  
  
    private static void getStuffInit(Scanner in) {
        size = in.nextInt();
        unitsPerPlayer = in.nextInt();
        myUnits = new ArrayList();
        enemyUnits = new ArrayList();
        for (int i=0; i<unitsPerPlayer; i++) {
            myUnits.add(new Unit());
            enemyUnits.add(new Unit());
        }
    }
    private static void getStuffEvent(Scanner in) {
        field = new char[size][size];
        for (int i = 0; i < size; i++) {
            char[] row = in.next().toCharArray();
            //System.out.println(row.length);
            for (int j = 0; j < size; j++) {
                field[j][i] = row[j];
            }
        }
        for (int i = 0; i < unitsPerPlayer; i++) {
            myUnits.get(i).x = in.nextInt();
            myUnits.get(i).y = in.nextInt();
        }
        for (int i = 0; i < unitsPerPlayer; i++) {
            enemyUnits.get(i).x = in.nextInt();
            enemyUnits.get(i).y = in.nextInt();
        }
        validActions = new ActionList();
        legalActions = in.nextInt();
        for (int i = 0; i < legalActions; i++) {
            String atype = in.next();
            int index = in.nextInt();
            String dir1 = in.next();
            String dir2 = in.next();
            validActions.add(new Action(atype,index,dir1,dir2));
        }
    }
  
    private static List<Space> nextTo(int x, int y) {
        List<Space> res = new LinkedList();
        res.add(new Space(x-1,y-1));
        res.add(new Space(x,y-1));
        res.add(new Space(x+1,y-1));
        res.add(new Space(x+1,y));
        res.add(new Space(x+1,y+1));
        res.add(new Space(x,y+1));
        res.add(new Space(x-1,y+1));
        res.add(new Space(x-1,y));
        return res;
    }
    private static List<Space> nextToValidMove(int x, int y) {
        List<Space> res = nextTo(x,y);
        return res.stream().filter((o) -> validMoveTo(o.x,o.y)).collect(Collectors.toList());
    }
    private static boolean validMoveTo(int x, int y) {
        if (x >= size || y >= size) return false;
        if (x < 0 || y < 0) return false;
        for (Unit u : enemyUnits) {
            if (u.x == x && u.y == y) return false;
        }
        for (Unit u : myUnits) {
            if (u.x == x && u.y == y) return false;
        }
        return field[x][y] != '.' && field[x][y] != '4';
    }
    private static char charOnSpace(Space s) {
        return field[s.x][s.y];
    }
    private static String directionTo(int playerIndex, int x, int y) {
        String res = "";
        Unit unit = myUnits.get(playerIndex);
        if (y < unit.y) res += "N";
        if (unit.y < y) res += "S";
        if (x < unit.x) res += "W";
        if (unit.x < x) res += "E";
        return res;
    }
  
  
    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        getStuffInit(in);
        // game loop
        while (true) {
            getStuffEvent(in);
            
            if (validActions.size() <= 0) continue;
            int bestActionPriority = 0;
            Action bestAction = validActions.get(0);
            
            //check if any unit can get on a 3 heigh thingy
            for (int i=0; i<myUnits.size(); i++) {
                for(Space space : nextToValidMove(myUnits.get(i).x, myUnits.get(i).y)) {
                    if (charOnSpace(myUnits.get(i)) == '2' && charOnSpace(space) == '3') {
                        bestActionPriority = 9999;
                        bestAction = new Action("MOVE&BUILD", i, directionTo(i, space.x, space.y), "S");
                    }
                }
            }
            
            //check if any unit can make a thingy 3 heigh
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            System.out.println(bestAction.toString() + " with priority:" + bestActionPriority);
        }
    }
}

class Unit extends Space {
    Unit() {
        super();
    }
}

class Space {
    int x;
    int y;
    
    Space() {
        x = -1;
        y = -1;
    }
    Space(int x, int y) {
        this.x = x;
        this.y = y;
    }
    @Override
    public String toString() {
        return "(" + x + "," + y + ")";
    }
}

class ActionList extends LinkedList<Action> {
    ActionList () {
        super();
    }
}

class Action {
    private String atype;
    private int playerIndex;
    private String dir1;
    private String dir2;
    
    Action(String actionString) {
        String[] res = actionString.split(" ");
        this.atype = res[0];
        this.playerIndex = Integer.parseInt(res[1]);
        this.dir1 = res[2];
        this.dir2 = res[3];
    }
    
    Action(String type, int player, String a, String b) {
        this.atype = type;
        this.playerIndex = player;
        this.dir1 = a;
        this.dir2 = b;
    }
    
    boolean matches(String s) {
        return this.toString().equals(s);
    }
    
    @Override
    public String toString() {
        return atype + " " + playerIndex + " " + dir1 + " " + dir2;
    }
}
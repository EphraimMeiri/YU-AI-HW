import connect4_2 as cn4
import random
import copy
import math
from timeit import default_timer as timer

 
 # What we're going to do: 
 #      1) A simple MC implementation, which just checks n random games on each move and takes the best move.
 #      2) A MCST, which saves the wins/tries of each node (representing a possible move at each point.)
 #          Each node represents a move, and each child is a subsequent move.
 #          Upon the completion of our search we will be able to examine the 1st level of nodes and select the one with 
 #              either the highest ratio, or (if we use UCB, see slides) the highest # of explorations 
 #          To arrive at estimation, we run n simulations. Each simulation Selects a node based on it's current score, 
 #              and continues to traverse it's children based on the same metric until the game ends. 
 #              When we reach this leaf node, we need to pass the result back up the tree 
 #                  it makes the most sense to do this implicitly, by making the traversal a recursive call to node.move(col) 
 #
 #          Selection: Explore the children of this node, choosing the one with the the Max UCB
 #              node.UCB := Q + c* sqrt(ln(node.depth)/node.count)
 #                  Q:= node.wins/node.count       
 #
n= 100
ucb_conf= 2
class Node:
    children= dict()
    depth=0
    count=0
    wins=0
    my_id=0
    parent=0
    color=cn4.BLUE_INT
    def __init__(self,d,col,clr,par) -> None:
        self.children= dict()
        self.count=0
        self.wins=0
        self.depth=d
        self.my_id=col
        self.color=clr
        self.parent=par
    
    def __del__(self):
        for child in self.children.items():
            del child
        self.children=None
    
    def get(self,col):
        # return self.children.get(col,Node(self.depth+1,col,self.color))
        if col in self.children:
            return self.children[col]
        else:
            self.children[col]= Node(self.depth+1,col,self.color,self)
            return self.children[col]

    def val(self):
        if self.count==0:
            return 0
        else:
            return self.wins/self.count
    
    def ucb(self):
        if self.parent is None:
            return -1 # UCB not relevant for Root.
        term2=0
        if self.count != 0:
            numer= math.log(self.parent.count)
            term2= ucb_conf * math.sqrt(numer/self.count)
        return self.val()+term2 

    # Returns the child node with max UCB score, given it is a valid spot.
    def get_max_ucb_child(self,board):
        for c in range(cn4.COLUMN_COUNT):
            self.get(c)
        if self.count==1:
            return random.choice(list(self.children.values()))
        else:
            # return max(self.children.items(), key=lambda child: child[1].ucb())[1]
            valid_cols= cn4.get_valid_locations(board)
            subset= [child for i,child in self.children.items() if i in valid_cols]
            if len(valid_cols) != cn4.COLUMN_COUNT:
                print("look here")
            return max(subset, key=lambda child: child.ucb())

        # ucbs= [(i,n.ucb(1)) for i,n in self.children.items() if i in cn4.get_valid_locations(board)]
        # ucbs.sort(key=lambda x: x[1])
        # return self.children[ucbs[0][0]]

    def root_exp(self,board):
        self.count+=1
        result= Node.get_max_ucb_child(self,board).move(board)
        self.wins+=result

    def explore(self,board):
        # Dont increment count, already incremented in move. 
        result= Node.get_max_ucb_child(self,board).move(board)
        self.wins+=result
        return result
    
    # Should the order of the move depend on our color?  
    def move(self,board):
        self.count+=1
        # We need to make sure the children exist.
        for c in range(cn4.COLUMN_COUNT):
            self.get(c)
        # Make the move this node represents.
        cn4.drop_in_col(board,self.my_id,self.color)
        if cn4.game_is_won(board,self.color):
            self.wins+=1
            return 1
        elif cn4.game_is_draw(board):
            return 0
        else: # We could not have lost with our own move, so we don't check for that. Continue with gameplay simulation.
            # Simulate a random move for the other player.
            column = random.choice(cn4.get_valid_locations(board))
            cn4.drop_in_col(board,column,cn4.other_color(self.color))
            if cn4.game_is_won(board,cn4.other_color(self.color)):
                return -1 # Should this be wins+=-1 ?? for a loss
            elif cn4.game_is_draw(board):
                return 0

            # If game is still in play, continue to explore best child.
            return self.explore(board) # This is a recursive call, which will call move on our best child.

def mcst_agent(board,color,display=True):
    start_time= timer()
    tree= Node(0,None,color,None)
    valid_locations = cn4.get_valid_locations(board)
    other_color= cn4.other_color(color)
    for i in range(7*n):
        board_copy=copy.deepcopy(board)
        tree.root_exp(board_copy)
    end_time= timer()
    move= tree.get_max_ucb_child(board).my_id
    if display:
        print("Move took ",end_time-start_time)
        print("moved @",move)
        scores= [child.ucb() for i,child in tree.children.items() if i in cn4.get_valid_locations(board)]
        print(scores)
    del tree
    cn4.drop_in_col(board,move,color)

def MCagent(board,color):
    ratios=[]
    valid_locations = cn4.get_valid_locations(board)
    other_color= cn4.other_color(color)
    for c in range(cn4.COLUMN_COUNT):
        if c not in valid_locations:
            ratios.append(-1)
        else:
            wins=0
            for i in range(n):
                board_copy= copy.deepcopy(board)
                cn4.drop_in_col(board_copy,c,color)
                if cn4.game_is_won(board_copy,color):
                    wins+=1
                    break
                elif cn4.game_is_over(board_copy):
                    break
                column = random.choice(cn4.get_valid_locations(board_copy))
                cn4.drop_in_col(board_copy,column,other_color)
                while(not cn4.game_is_over(board_copy)):
                    column = random.choice(cn4.get_valid_locations(board_copy))
                    cn4.drop_in_col(board_copy,column,color)
                    if cn4.game_is_won(board_copy,color):
                        wins+=1
                        break
                    elif cn4.game_is_over(board_copy):
                        break
                    column = random.choice(cn4.get_valid_locations(board_copy))
                    cn4.drop_in_col(board_copy,column,other_color)
            ratios.append(wins/n)
    move= ratios.index(max(ratios))
    return move

def mc_simple_agent(board,color,display=False):
    start_time= timer()
    ratios=[]
    valid_locations = cn4.get_valid_locations(board)
    other_color= cn4.other_color(color)
    for c in range(cn4.COLUMN_COUNT):
        if c not in valid_locations:
            ratios.append(-1)
        else:
            wins=0
            for i in range(n):
                board_copy= copy.deepcopy(board)
                cn4.drop_in_col(board_copy,c,color)
                if cn4.game_is_won(board_copy,color):
                    wins+=1
                    break
                elif cn4.game_is_over(board_copy):
                    break
                # cn4.muskenu(board_copy,other_color,debugging=False)
                column = random.choice(cn4.get_valid_locations(board_copy))
                cn4.drop_in_col(board_copy,column,other_color)
                while(not cn4.game_is_over(board_copy)):
                    column = random.choice(cn4.get_valid_locations(board_copy))
                    cn4.drop_in_col(board_copy,column,color)
                    if cn4.game_is_won(board_copy,color):
                        wins+=1
                        break
                    elif cn4.game_is_over(board_copy):
                        break
                    # cn4.muskenu(board_copy,other_color,debugging=False)
                    column = random.choice(cn4.get_valid_locations(board_copy))
                    cn4.drop_in_col(board_copy,column,other_color)
            ratios.append(wins/n)
    end_time= timer()
    print("Move took ",end_time-start_time)
    if display:
        print(ratios)
    move= ratios.index(max(ratios))
    return move
    cn4.drop_in_col(board,move,color)


# cn4.play(cn4.hakham,mcst_agent,True)
# cn4.play(cn4.MoveRandom,mcst_agent)
score=0
tied=0
for i in range(0,15):
    print(i,end="\t")
    result=cn4.play(cn4.hakham,mc_simple_agent,False)
    if (result==cn4.BLUE_INT):
        score+=1    
    elif result=="Draw":
        tied+=1
print(score,"games won by BLUE agent, ",tied,"Tied")
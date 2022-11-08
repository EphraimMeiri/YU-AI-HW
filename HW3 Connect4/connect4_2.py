import copy
from itertools import count
import numpy as np
import math
import random
import re
from termcolor import colored  # can be taken out if you don't like it...

# # # # # # # # # # # # # # global values  # # # # # # # # # # # # # #
ROW_COUNT = 6
COLUMN_COUNT = 7

RED_CHAR = colored('X', 'red')  # RED_CHAR = 'X'
BLUE_CHAR = colored('O', 'blue')  # BLUE_CHAR = 'O'

EMPTY = 0
RED_INT = 1
BLUE_INT = 5


# # # # # # # # # # # # # # functions definitions # # # # # # # # # # # # # #

def create_board():
    """creat empty board for new game"""
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


def drop_chip(board, row, col, chip):
    """place a chip (red or BLUE) in a certain position in board"""
    board[row][col] = chip


def is_valid_location(board, col):
    """check if a given column in the board has a room for extra dropped chip"""
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    """assuming column is available to drop the chip,
    the function returns the lowest empty row  """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """print current board with all chips put in so far"""
    # print(np.flip(board, 0))
    print(" 1 2 3 4 5 6 7 \n" "|" + np.array2string(np.flip(np.flip(board, 1)))
          .replace("[", "").replace("]", "").replace(" ", "|").replace("0", "_")
          .replace(str(RED_INT), RED_CHAR).replace(str(BLUE_INT), BLUE_CHAR).replace("\n", "|\n") + "|")

def game_is_over(board):
    if game_is_won(board,RED_INT):
        return True
    elif game_is_won(board,BLUE_INT):
        return True
    elif len(get_valid_locations(board))==0:
        return True
    else:
        return False

def game_is_won(board, chip):
    """check if current board contain a sequence of 4-in-a-row of in the board
     for the player that play with "chip"  """

    winning_Sequence = np.array([chip, chip, chip, chip])
    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if ("".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[r, :])))):
            return True
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if ("".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[:, c])))):
            return True
    
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board.diagonal(offset)))):
            return True
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            return True

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def MoveRandom(board, color):
    valid_locations = get_valid_locations(board)
    column = random.choice(valid_locations)   # you can replace with input if you like... -- line updated with Gilad's code-- thanks!
    row = get_next_open_row(board, column)
    if get_next_open_row is None:
        print("ERROR!")
    drop_chip(board, row, column, color)


##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
# # # # # # # # # # # # # # NEW FUNCTIONS # # # # # # # # # # # # # #
def drop_in_col(board,col,color):
    if(is_valid_location(board,col)):
        drop_chip(board,get_next_open_row(board,col),col,color)
    else:
        print("ILLEGAL MOVE ATTEMPTED")

def color_str(color):
    if color==RED_INT:
        return "RED"
    if color==BLUE_INT:
        return "BLUE"


def other_color(color):
    if color== BLUE_INT:
        return RED_INT
    if color==RED_INT:
        return BLUE_INT


# Minimally inteligent agent-- see potential wins (and move or block as appropriate)
def muskenu(board,color): # חכמת המסכן בזויה  muškēnu if we're being pedantic...
    winning_move= next_move_win(board,color)
    urgent_block= should_block(board,color)
    if winning_move is not None:
        row=get_next_open_row(board,winning_move)
        print("muškēnu",color_str(color),"goes for the win at (",row,",",winning_move,")")
        drop_in_col (board,winning_move,color)
    elif urgent_block is not None:
        row=get_next_open_row(board,urgent_block)
        print("muškēnu",color_str(color),"blocks at (",row,",",urgent_block,")")
        drop_in_col(board,urgent_block,color)
    else:
        MoveRandom(board,color)

# def muskenu2(board,color): # חכמת המסכן בזויה  muškēnu if we're being pedantic...
    spots= get_valid_locations(board)
    for spot in spots:
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,color)
        if game_is_won(tmp,color):
            drop_in_col(board,spot,color)
            print("muškēnu2",color_str(color),"goes for the win at c",spot)
            return
    for spot in spots:
        other= other_color(color)
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,other)
        if game_is_won(tmp,other):
            drop_in_col(board,spot,color)
            print("muškēnu2",color_str(color),"blocks at c",spot)
            return
    MoveRandom(board,color)

def hakham(board,color): # חכמת המסכן בזויה  muškēnu if we're being pedantic...
    spots= get_valid_locations(board)
    winning_move= next_move_win(board,color)
    if winning_move != None:
        drop_in_col(board,winning_move,color)
    for spot in spots:
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,color)
        if game_is_won(tmp,color):
            drop_in_col(board,spot,color)
            print("muškēnu2",color_str(color),"goes for the win at c",spot)
            return spot
    for spot in spots:
        other= other_color(color)
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,other)
        if game_is_won(tmp,other):
            drop_in_col(board,spot,color)
            print("muškēnu2",color_str(color),"blocks at c",spot)
            return spot
    for spot in spots:
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,color)
        moves= winning_moves(tmp,color)
        if len(moves)>1:
            drop_in_col(board,spot,color)
            print("muškēnu2",color_str(color),"goes for the trap at c",spot)
            return spot

    for spot in spots:
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,color)
        moves= winning_moves(tmp,other)
        if len(moves)>1:
            drop_in_col(board,spot,color)
            print("muškēnu2",color_str(color),"blocks trap at c",spot)
            return spot
    
    # MoveRandom(board,color)
    ab_agent(board,color)

# Used to identify an immediate win.
def next_move_win(board,color):
    spots= get_valid_locations(board)
    for spot in spots:
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,color)
        if game_is_won(tmp,color):
            return spot
    return None # No winning moves.

# returns a list of moves that would result in color wining. 
# Used to identify double traps
def winning_moves(board,color):
    spots= get_valid_locations(board)
    wins= []
    for spot in spots:
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,color)
        if game_is_won(tmp,color):
            wins.append(spot)
    return wins

# Should color block a given move? If the oponent can win, then we should steal it.
def should_block(board,color):
    return next_move_win(board,other_color(color))

# Evaluate a 4 chip sequence-- add for BLUE sequences, and subtract for RED.
def sum_scores(group_sum):
    score=0
    if group_sum== 2:
        score-=1
    if group_sum== 3:
        score-= 5
    if group_sum== 4:
        return float("-inf")
    if group_sum== 10:
        score+= 1
    if group_sum== 15:
        score+= 5
    if group_sum== 20:
        return float("inf")
    return score

# Huristic evaluation of the boad. 
# If the board is a win, return +-∞ immediatly.
# if there is a double trap from here, return a very large value
def eval(board_copy):
    score=0
    chip=BLUE_INT
    other= other_color(chip)
    winning_options= winning_moves(board_copy,chip)

    # If the board is a win, return +-∞ immediatly.
    if game_is_won(board_copy,chip):
        return float("inf")
    if game_is_won(board_copy,other):
        return float("-inf")
    
    # if there is a double trap from here, return a very large value
    if (winning_options is not None) and len(winning_options)>1:
        return float("10000") # We got a golden ticket right here.
    losing_options= winning_moves(board_copy,other_color(chip))
    if (losing_options is not None) and len(losing_options)>1:
        return float("-10000") # He got a golden ticket right here.
    
    # Add 4-sums in Horizontal 
    for r in range(ROW_COUNT):
        for bound in range(ROW_COUNT-4):
            row= board_copy[r,bound:bound+4]
            group_sum= sum(row)
            score+=sum_scores(group_sum)
    # Add 4-sums in Vertical 
    for c in range(COLUMN_COUNT):
        for bound in range(COLUMN_COUNT-4):
            col= board_copy[bound:bound+4,c]
            group_sum= sum(row)
            score+=sum_scores(group_sum)
    # Add from positively sloped diagonals
    for offset in range(-2, 4):
        diag=board_copy.diagonal(offset)
        for bound in range(len(diag)-4):
            row= diag[bound:bound+4]
            group_sum= sum(row)
            score+=sum_scores(group_sum)
    # Add from negatively sloped diagonals
    for offset in range(-2, 4):
        diag=np.flip(board_copy, 1).diagonal(offset)
        for bound in range(len(diag)-4):
            row= diag[bound:bound+4]
            group_sum= sum(row)
            score+=sum_scores(group_sum)
    return score


# MiniMax
def maxi(board,d):
    # If we've reached a leaf, return the eval of this board. The move (0) returned is not significant.
    if d==0 or game_is_won(board,BLUE_INT) or (len(get_valid_locations(board))==0):
        output=[eval(board),0]
        return output

    v= float("-inf") # v stores the current maxVal, so we begin with the minimal possible value
    ns= get_valid_locations(board) # List of valid moves
    bestMove= 0
    # Check the eval for each possible future board, via recursive minimax calls, and then return the the best predicted option.
    for col in ns: 
        hypothetical_board= copy.deepcopy(board)
        drop_in_col(hypothetical_board,col,BLUE_INT)
        if game_is_won(hypothetical_board,BLUE_INT):
            return [float("inf"),col]
        min= mini(hypothetical_board,d-1)
        if min[0]>v:
            v = min[0]
            bestMove=col
    output=[v,bestMove]
    return output

# Mini is the mirror of max-- it calls max for the next move, and find the minimal value from the options.
def mini(board,d):
    if (len(get_valid_locations(board))==0):
        print("ran to tie")
    if d==0 or game_is_over(board):
        output=[eval(board),0]
        return output
    v= float("inf")
    ns= get_valid_locations(board)
    bestMove=random.choice(ns)
    for col in ns:
        hypothetical_board= copy.deepcopy(board)
        drop_in_col(hypothetical_board,col,RED_INT)
        if game_is_won(hypothetical_board,RED_INT):
            return [float("-inf"),col]
        max= maxi(hypothetical_board,d-1)
        if max[0]<v:
            v= max[0]
            bestMove=col
    output=[v,bestMove]
    return output

# Returns the best column to pick given the current board, assuming the oponent plays optimally
# Aß from slides
# s= state (board copy), 
# d= depth-- passed in initial call = # of moves down to check. 
# a,b= alpha (max) beta (min)
# Define max to be BLUE and min to be RED
# Generally follows the same structure as minimax, with the addition of maintaining overall min and max values.
# These allow for the pruining in lines 364-367
def abmax(board,d,a,b):
    if d==0 or game_is_over(board):
        output=[eval(board),0]
        return output
    v= float("-inf")
    ns= get_valid_locations(board)
    bestMove= random.choice(ns)
    for col in ns:
        hypothetical_board= copy.deepcopy(board)
        drop_in_col(hypothetical_board,col,BLUE_INT)
        min= abmin(hypothetical_board,d-1,a,b)
        if min[0]>v:
            v = min[0]
            bestMove=col
        if v>=b:            # <-- Pruning
            return [v,col]
        if v>a:
            a=v
    output=[v,bestMove]
    return output

def abmin(board,d,a,b):
    if d==0 or game_is_over(board):
        output=[eval(board),0]
        return output
    v= float("inf")
    ns= get_valid_locations(board)
    bestMove=random.choice(ns)
    for col in ns:
        hypothetical_board= copy.deepcopy(board)
        drop_in_col(hypothetical_board,col,RED_INT)
        max= abmax(hypothetical_board,d-1,a,b)

        if max[0]<v:
            v= max[0]
            bestMove=col
        if v<=a:
            return [v,col]
        if v<a:
            b=v
    output=[v,bestMove]
    return output

# Call minimax, but shortcut the forward checking if there is an immediate win to to take or prevent.
def minimax_agent(board,color):
    winning_move=next_move_win(board,color)
    block=should_block(board,color)
    if winning_move != None:
        drop_in_col(board,next_move_win(board,color),color)
    elif block != None:
        drop_in_col(board,block,color)
    else:
        depth= 2
        if color== BLUE_INT:
            move= maxi(board,depth)[1]
            drop_in_col(board,move,BLUE_INT)
        elif color==RED_INT:
            move= mini(board,depth)[1]
            drop_in_col(board,move,RED_INT)

# Call alpha-beta, but shortcut the forward checking if there is an immediate win to to take or prevent.
def ab_agent(board,color):
    winning_move=next_move_win(board,color)
    block=should_block(board,color)
    if winning_move != None:
        drop_in_col(board,winning_move,color)
        return winning_move
    elif block != None:
        drop_in_col(board,block,color)
        return block
    else:
        depth= 3
        if color== BLUE_INT:
            move= abmax(board,depth,float("-inf"),float("inf"))[1]
            drop_in_col(board,move,BLUE_INT)
            return move
        elif color==RED_INT:
            move= abmin(board,depth,float("-inf"),float("inf"))[1]
            drop_in_col(board,move,RED_INT)
            return move

# Just evalutate the immediate options, equivalent to d=1 forward checking.
def eval_agent(board,color):
    spots= get_valid_locations(board)
    tmp = copy.deepcopy(board)
    drop_in_col(tmp,spots[0],color)
    max_val= eval(tmp)
    col= spots[0]
    for spot in spots:
        tmp = copy.deepcopy(board)
        drop_in_col(tmp,spot,color)
        score= eval(tmp)
        if score > max_val:
            max_val= score
            col=spot
    drop_in_col(board,col,color)
##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
# # # # # # # # # # # # # # main execution of the game # # # # # # # # # # # # # #
def human_move(board,color):
    col = int(input(color_str(color),"please choose a column(1-7): "))
    while col > 7 or col < 1:
        col = int(input("Invalid column, pick a valid one: "))
    while not is_valid_location(board, col - 1):
        col = int(input("Column is full. pick another one..."))
    col -= 1

    row = get_next_open_row(board, col)
    drop_chip(board, row, col, color)

def play(player1,player2,printing=True):
    turn = 0

    board = create_board()
    print_board(board)
    game_over = False
    player=player1
    color= RED_INT
        
    while not game_over:
        if turn % 2 == 0:
            player=player1
            color= RED_INT
        if turn % 2 == 1 and not game_over:
            player=player2
            color=BLUE_INT
        
        if player=="human":
            human_move(board,color)
        elif player=="muskenu":
            muskenu(board,color)
        elif player=="hakham":
            hakham(board,color)
        elif player=="minimax":
            minimax_agent(board,color)
        elif player=="ab":
            ab_agent(board,color)
        elif player=="eval":
            eval_agent(board,color)
        elif player=="rand":
            MoveRandom(board,color)
        else:
            print("INVALID PLAYER")
            return
        
        if printing:
            print_board(board)
        
        if game_is_won(board, RED_INT):
            game_over = True
            print(colored("Red wins!", 'red'))
            return RED_INT
        if game_is_won(board, BLUE_INT):
            game_over = True
            print(colored("Blue wins!", 'blue'))
            return BLUE_INT
        if len(get_valid_locations(board)) == 0:
            game_over = True
            return "Draw"
            print(colored("Draw!", 'blue'))
        turn += 1


score=0
tied=0
for i in range(0,100):
    result=play("ab","hakham")
    if (result==BLUE_INT):
        score+=1
    elif result=="Draw":
        tied+=1

print(score,"games won by BLUE agent, ",tied,"Tied")

#TODO: Package agent as appropriate
def agent1move(board):
    board_copy= copy.deepcopy(board)
    return hakham(board_copy,BLUE_INT)
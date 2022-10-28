# -*- coding: utf-8 -*-
"""DFS_queens.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1puD0kHn_0jLIZbtEOzNW4Atp2JNHcaYB

This is the notebook version of the code. I will use this to explain the homework.  I used parts of the code from: https://www.sanfoundry.com/python-program-solve-n-queen-problem-without-recursion/

As we did in class, we will represent the board as a one-dimensional array where each position in the arrray is the n'th queen's column value. So if the array is: [1, 3, 0, 2], then the first queen is in position 1 (from 0--3), the second queen is in position 3 (the last column), the third queen is in the first column and the last queen is the in the second position.
"""

columns = [] #columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
size = 4
import random

def place_n_queens(size):
    columns.clear()
    row = 0
    while row < size:
        column=random.randrange(0,size)
        columns.append(column)
        row+=1


def display():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()


# Provided dfs method.
def solve_queen(size):
    columns.clear()
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0  
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        #place queen in next row
        ''''print(columns)
        print("I have ", row, " number of queens put down")
        display()
        print(number_of_moves)'''
        while column < size:
            number_of_iterations+=1
            if next_row_is_safe(column):
                place_in_next_row(column)
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if (column == size or row == size):
            number_of_iterations+=1
            # if board is full, we have a solution
            if row == size:
                print("I did it! Here is my solution")
                display()
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            if (prev_column == -1): #I backtracked past column 1
                print("There are no solutions")
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column
"""
    NEW CODE
"""
# This empty board method is used in stead of columns.clear for the board used to place rows in arbitrary order.
def empty_board():
    columns.clear()
    print(columns)
    for i in range(0,size):
        columns.append(-1)



# returns a list of rows that conflict with this row.
# Used as a heuristic for optimal placement in repair.
# Same logic as that provided next_row_is_safe method.
def get_conflicts(myRow):
   myCol= columns[myRow]
   conflicts=[]
   if myCol==-1:
       return conflicts
   # Check column
   for row,col in enumerate(columns):
     if col==myCol and row!=myRow and col!=-1:
      #  print("Col hit (row,col)", row, col)
       conflicts.append(row)

   # check diagonal
   for queen_row, queen_column in enumerate(columns):
    if queen_row==myRow:
      continue #This is just me.
    elif queen_column==-1:
        continue
    elif (queen_column - queen_row) == (myCol-myRow):
      # print("Diagonal hit(row,col)", row, col)
      # print(queen_column,queen_row,myCol,myRow)
      # print((queen_column - queen_row), "==", (myCol-myRow))
      conflicts.append(row)

   # check other diagonal
   for queen_row, queen_column in enumerate(columns):
    if queen_row==myRow:
      continue      #This is just me.
    elif queen_column == -1:
      continue
    elif ((size - queen_column) - queen_row
          == (size - myCol) - myRow):
          # print("Other Diagonal hit(row,col)", row, col)
          conflicts.append(row)
   return conflicts

# Used as a sub-routine for the whole board correctness check.
def col_is_valid(myRow):
   myCol= columns[myRow]
   if myCol==-1:
       return True
   # Check column
   for row,col in enumerate(columns):
     if col==myCol and row!=myRow and col!=-1:
      #  print("Col hit (row,col)", row, col)
       return False

   # check diagonal
   for queen_row, queen_column in enumerate(columns):
    if queen_row==myRow:
      continue #This is just me.
    elif queen_column==-1:
        continue
    elif (queen_column - queen_row) == (myCol-myRow):
      # print("Diagonal hit(row,col)", row, col)
      # print(queen_column,queen_row,myCol,myRow)
      # print((queen_column - queen_row), "==", (myCol-myRow))
      return False

   # check other diagonal
   for queen_row, queen_column in enumerate(columns):
    if queen_row==myRow:
      continue      #This is just me.
    elif queen_column == -1:
      continue
    elif ((size - queen_column) - queen_row
          == (size - myCol) - myRow):
          # print("Other Diagonal hit(row,col)", row, col)
          return False
   return True

def board_is_valid():
  # for row,col in enumerate(columns):
  #   print(row,col)
  for i in range(0,size):
    # print()
    # print("I:",i)
    if not col_is_valid(i):
      return False
  return True

# Checks not only for conflicts, but also that all pieces were actually placed.
def all_placed_correctly():
    for row in columns:
        if columns[row]==-1:
            return False
    if board_is_valid():
        return True
    else:
        return False

# Returns list of columns for which the passed row has no conflicts.
def potential_cols(row):
    available_cols=[]
    available=True
    # check column
    for column in range(0,size):
        available=True
        for queen_column in columns:
            if queen_column==-1:
                continue
            elif column == queen_column:
                available= False

        # check diagonal
        for queen_row, queen_column in enumerate(columns):
            if queen_column==-1:
                continue
            elif queen_column - queen_row == column - row:
                available= False

        # check other diagonal
        for queen_row, queen_column in enumerate(columns):
            if queen_column==-1:
                continue
            elif ((size - queen_column) - queen_row == (size - column) - row):
                available= False
        if available:
            available_cols.append(column)
    return available_cols

# Spots is the proxy model for forward checking.
# Maintains a list of available spots for each row.
def init_spots():
    spots= []
    for r in range(0,size):
        spots.append([c for c in range(0,size)]) # We begin with all spots being available.
    return spots

# When a new piece is placed we remove the conflicting spots.
def block_spots(row,col,origspots):
    spots= [row.copy() for row in origspots]
    for r in spots:
        if col in r:
            r.remove(col)
    # check diagonal
    for r in range(0,size):
        for c in origspots[r]:
            if ((c-r == col-row) or ((size - c) - r == (size - col) - row))and (c in spots[r]):
                spots[r].remove(c)
    return spots

# Used to re-create the spots array when backtracking.
def redo_spots(columns):
    spots=init_spots()
    for row,col in enumerate(columns):
        if col != -1:
            spots[row].clear()
            spots=block_spots(row,col,spots)
    return spots

# A helper method to print the passed spots array.
def disp_spots(spots):
    for c in range(0,size):
        print(c,end="  ")
    print()
    for r in range(0,size):
        for c in range(0,size):
            if c in spots[r]:
                print("+",end="  ")
            else:
                print("-",end="  ")
        print()

# Does all unplaced rows (except the exceptrow) have a place to go
# Could be improved by placing pieces with only one potential spot.
def spots_remaining(spots,exceptrow):
    for row,col in enumerate(columns):
        if col==-1 and (not (row == exceptrow)) and len(spots[row])==0:
            print("No spots for r",row)
            return False
    return True

# Returns the row with the fewest potential spots.
def most_restricted(spots):
    remaining= [r for r in range(0,size) if columns[r]==-1]
    min_row= 0
    min= size+1
    # print("-")
    for r in remaining:
        opt= len(spots[r])
        if opt< min:
            min=opt
            min_row=r
    # print("Most restricted ",min_row,'\t',min)
    return min_row


def solve_forward_checking(size):
    empty_board()
    number_of_moves = 0  # where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0
    row = 0
    column = 0
    col_max=0
    # Spots is the array keeping track of which spots are available (0) or not (-1).
    spots= init_spots()

    # iterate over rows of board
    while True:
        # place queen in next row
        ''''print(columns)
        print("I have ", row, " number of queens put down")
        display()
        print(number_of_moves)'''
        if spots[row]:
            col_max=max(spots[row])
        else:
            col_max=-1
        for col in spots[row]:
            column=col
            number_of_iterations += 1
            new_spots= block_spots(row,col,spots)
            spots_remain= True
            for r,c in enumerate(columns):
                if c==-1 and (not (r == row)) and len(new_spots[r])==0:
                    spots_remain= False
                    break
            if spots_remain:    # We found a good spot for this row, continue to next row.
                number_of_moves += 1
                columns[row] = col
                spots = new_spots
                spots[row].clear()
                # disp_spots(spots)
                row +=1
                break
            else:           # We will ruin the board with this placement.
                column+=1 # Used as an indicator of passing the last available col
                continue


        if (column>col_max or row == size): # If we've iterated to the end of the board.
            if (all_placed_correctly()):
                print("I did it! Here is my solution")
                display()
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            else:             # I couldn't find a solution so I now backtrack
                number_of_moves      += 1
                if (row==0):  # I backtracked past 1st row.
                    print("There are no solutions")
                    # print(number_of_moves)
                    return number_of_iterations, number_of_moves
                prev_row= row-1
                prev_column = columns[prev_row]
                columns[prev_row]=-1
                spots = redo_spots(columns)
                # Since I am using the for col in spots we preemptively remove the previously tried columns
                # This is equivalent to colum+=1 in the DFS code.
                spots[prev_row]=[spot for spot in spots[prev_column] if spot>prev_column]
                # try previous row again
                row = prev_row


def solve_forward_checking_most_constricted(size,start_row=2):
    empty_board()
    number_of_moves = 0  # where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0
    # row = int(size/2)
    row = start_row
    row_stack=[]
    column = 0
    col_max=0
    # Spots is the array keeping track of which spots are available (0) or not (-1).
    spots= init_spots()

    # iterate over rows of board
    while True:
        # place queen in next row
        ''''print(columns)
        print("I have ", row, " number of queens put down")
        display()
        print(number_of_moves)'''
        if spots[row]:
            col_max=max(spots[row])
        else:
            col_max=-1
        for col in spots[row]:
            column=col
            number_of_iterations += 1
            new_spots= block_spots(row,col,spots)
            spots_remain= True
            for r,c in enumerate(columns):
                if c==-1 and (not (r == row)) and len(new_spots[r])==0:
                    spots_remain= False
                    break
            if spots_remain:    # We found a good spot for this row, continue to next row.
                number_of_moves += 1
                columns[row] = col
                spots = new_spots
                spots[row].clear()
                # disp_spots(spots)
                row_stack.append(row)
                row = most_restricted(spots)
                break
            else:           # We will ruin the board with this placement.
                column+=1 # Used as an indicator of passing the last available col
                continue


        if (column>col_max): # If we've iterated to the end of the board.
            if (all_placed_correctly()):
                print("I did it! Here is my solution")
                display()
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            else:             # I couldn't find a solution so I now backtrack
                number_of_iterations += 1
                number_of_moves      += 1

                if (not row_stack):  # I backtracked past 1st row.
                    print("There are no solutions")
                    # print(number_of_moves)
                    return number_of_iterations, number_of_moves
                prev_row= row_stack.pop()
                prev_column = columns[prev_row]
                columns[prev_row]=-1
                spots = redo_spots(columns)
                spots[prev_row]=[spot for spot in spots[prev_column] if spot>prev_column]
                # try previous row again
                row = prev_row


def solve_repair_very_random():
    empty_board()
    place_n_queens(size)
    display()
    moves= 4
    iterations=0
    while not board_is_valid():
        iterations+=1
        row= random.randrange(0,size)
        orig_col= columns[row]
        best_col= orig_col
        min_conflicts=len(get_conflicts(row))
        for c in range(0,size):
            columns[row]= c
            conflicts=len(get_conflicts(row))
            if conflicts<min_conflicts:
                min_conflicts=conflicts
                best_col=c
        if best_col==orig_col:
            print("No change")
        else:
            moves+=1
            columns[row]=best_col
            print(row,": Moved from ",orig_col," to ",best_col)
    print("Did it!")
    display()
    print(columns)
    return iterations,moves


def solve_repair_deadend_random():
    empty_board()
    place_n_queens(size)
    display()
    moves= 4
    iterations=0
    while not board_is_valid():
        iterations+=1
        row= random.randrange(0,size)
        max_conflicts= len(get_conflicts(row))
        for r in range(0,size):
            conflicts =len(get_conflicts(r))
            if conflicts>max_conflicts:
                row=r
                max_conflicts=conflicts
        orig_col= columns[row]
        best_col= orig_col
        min_conflicts=len(get_conflicts(row))
        for c in range(0,size):
            columns[row]= c
            conflicts=len(get_conflicts(row))
            if conflicts<min_conflicts:
                min_conflicts=conflicts
                best_col=c
        if best_col==orig_col:
            print("No change")
            place_n_queens(size)
        else:
            moves+=1
            columns[row]=best_col
            print(row,": Moved from ",orig_col," to ",best_col)
    print("Did it!")
    display()
    print(columns)
    return iterations,moves


def place_in_next_row(column):
    columns.append(column)
 
def remove_in_current_row():
    if len(columns) > 0:
        return columns.pop()
    return -1

def next_row_is_safe(column):
    row = len(columns) 
    # check column
    for queen_column in columns:
        if column == queen_column:
            return False
 
    # check diagonal
    for queen_row, queen_column in enumerate(columns):
        if queen_column - queen_row == column - row:
            return False
 
    # check other diagonal
    for queen_row, queen_column in enumerate(columns):
        if ((size - queen_column) - queen_row
            == (size - column) - row):
            return False
    return True


# #size = int(input('Enter n: '))
# num_iterations=0
# number_moves = 0
# #for i in range(0, 100):
# #    columns = [] #columns is the locations for each of the queens
# num_iterations, number_moves=solve_queen(size)
# print(num_iterations)
# print(columns)
size=8
empty_board()
display()


# count=0
# while not all_placed_correctly():
#     count+=1
#     place_best()
# print("count: ",count)

# print(solve_repair_very_random())
# print(solve_queen(size))

# print(solve_repair_deadend_random())
# size=20
# iter=[]
# moves=[]
# for i in range(0,size):
#    itt,mov= solve_forward_checking_most_constricted(size,i)
#    iter.append(itt)
#    moves.append(mov)
# print(min(iter),"\t",iter.index(min(iter)))
# print(min(moves),"\t",moves.index(min(moves)))
# print("hi")
# # print(solve_forward_checking_most_constricted(size))
# # print(solve_queen(size))
# print(columns)
size=8
print(solve_forward_checking(size))


# Forward Checking statistics
iterations=[]
moves=[]
for i in range(0,100):
    i,m=solve_repair_very_random()
    iterations.append(i)
    moves.append(m)
print("min\tmax\tavg")
print(min(iterations),'\t',max(iterations),'\t',(sum(iterations)/len(iterations)),"\tIterations")
print(min(moves),'\t',max(moves),'\t',(sum(moves)/len(moves)),"\tMoves")
import check
import math

# You can play minesweeper online here: http://minesweeperonline.com/

# A MineGrid is a (listof (listof Bool))
# Requires:  All lists are non-empty
#            Each (listof Bool) has the same length 

# note: True means mine, False means safe

# A MineBoard is a (listof (listof Str))
# Requires: Each string is either a mine ('*') hidden(' ')
#             or safe (a digit between '0' and '8')
#           All lists are non-empty
#           Each (listof Str) has the same length



# Example boards

grid1x1 = [[True]]

grid1x2 = [[False,True]]

grid1x5 = [[False,True,False,True,False]]

grid3x1 = [[True],
           [False],
           [True]]

grid5x1 = [[True],
           [False],
           [True],
           [False],
           [True]]

grid2x3 = [[True,False,False],
           [False,False,True]]


grid3x3 = [[True,False,False],
           [False,False,False],
           [False,False,True]]

grid4x3 = [[True,False,False,True],
           [False,True,False,False],
           [False,True,False,True]]

grid7x6 = [[False,True,True,False,True,False],
           [True,False,False,False,False,False],
           [False,False,False,True,True,False],
           [True,True,False,False,True,True],
           [False,False,False,False,True,False],
           [False,True,False,True,False,True],
           [False,False,False,False,False,True]]


# reveal(grid,board, row, col) reveals the tile at the given row and col(umn)
#   in board, using the mine positions from grid
# reveal: MineGrid MineBoard -> None
# requires: grid and board have the same dimensions and are consistent
#           0 <= row < height of board
#           0 <= col < width  of board
# effects: board is mutated

def reveal(grid,board,row,col):
    if grid[row][col]:
        board[row][col] = '*'
    else:
        board[row][col] = str(count_mines(grid,row,col))


# count_mines_check(grid,row,col) consumes a MineGrid, a natural number (row) 
#     and another natural number (col). The natural numbers represent a row and 
#     column within the MineGrid, and start counting from 0 (e.g. the top left 
#     is row == 0 col == 0). The function returns how many mine tiles are 
#     adjacent to the tile at that position.
# count_mines: MineGrid Nat Nat -> Nat
# requires: grid and board have the same dimensions and are consistent
#           0 <= row < height of board
#           0 <= col < width  of board
# Examples:
#     count_mines_check(grid1x1,0,0) => 1
#     count_mines_check(grid3x3,1,1) => 2

def count_mines_check(grid,row,col):
    if row == len(grid) or col == len(grid[0]) \
         or row < 0 or col < 0:
        return 0    
    elif grid[row][col] == True:
        return 1
    else:
        return 0
    
# count_mines(grid,row,col) consumes a MineGrid, a natural number (row) and 
#     another natural number (col). The natural numbers represent a row and 
#     column within the MineGrid, and start counting from 0 (e.g. the top left 
#     is row == 0 col == 0). The function returns how many mine tiles are 
#     adjacent to the tile at that position.
# count_mines: MineGrid Nat Nat -> Nat
# requires: grid and board have the same dimensions and are consistent
#           0 <= row < height of board
#           0 <= col < width  of board
# Examples:
#     count_mines(grid1x1,0,0) => 0
#     count_mines(grid3x3,1,1) => 2

def count_mines(grid,row,col):
    return count_mines_check(grid,row,col-1) \
           + count_mines_check(grid,row,col+1)\
           + count_mines_check(grid,row-1,col) \
           + count_mines_check(grid,row-1,col-1) \
           + count_mines_check(grid,row-1,col+1) \
           + count_mines_check(grid,row+1,col) \
           + count_mines_check(grid,row+1,col-1) \
           + count_mines_check(grid,row+1,col+1)

# Tests:
check.expect("q3t1", count_mines(grid1x1,0,0),0)
check.expect("q3t2", count_mines(grid1x2,0,0),1)
check.expect("q3t3", count_mines(grid1x2,0,1),0)
check.expect("q3t4", count_mines(grid1x5,0,0),1)
check.expect("q3t5", count_mines(grid1x5,0,3),0)
check.expect("q3t6", count_mines(grid1x5,0,4),1)
check.expect("q3t7", count_mines(grid3x1,0,0),0)
check.expect("q3t8", count_mines(grid3x1,1,0),2)
check.expect("q3t9", count_mines(grid3x1,2,0),0)
check.expect("q3t10", count_mines(grid5x1,0,0),0)
check.expect("q3t11", count_mines(grid5x1,1,0),2)
check.expect("q3t12", count_mines(grid5x1,4,0),0)
check.expect("q3t13", count_mines(grid2x3,0,0),0)
check.expect("q3t14", count_mines(grid2x3,0,1),2)
check.expect("q3t15", count_mines(grid2x3,0,2),1)
check.expect("q3t16", count_mines(grid2x3,1,0),1)
check.expect("q3t17", count_mines(grid2x3,1,1),2)
check.expect("q3t18", count_mines(grid2x3,1,2),0)
check.expect("q3t19", count_mines(grid3x3,0,0),0)
check.expect("q3t20", count_mines(grid3x3,0,1),1)
check.expect("q3t21", count_mines(grid3x3,0,2),0)
check.expect("q3t22", count_mines(grid3x3,1,0),1)
check.expect("q3t23", count_mines(grid3x3,1,1),2)
check.expect("q3t24", count_mines(grid3x3,1,2),1)
check.expect("q3t25", count_mines(grid3x3,2,0),0)
check.expect("q3t26", count_mines(grid3x3,2,1),1)
check.expect("q3t27", count_mines(grid3x3,2,2),0)
check.expect("q3t28", count_mines(grid4x3,1,1),2)
check.expect("q3t29", count_mines(grid4x3,1,2),4)
check.expect("q3t30", count_mines(grid7x6,3,3),4)
check.expect("q3t31", count_mines(grid7x6,5,1),0)
check.expect("q3t32", count_mines(grid7x6,1,5),2)

# Example boards

grid2x2 = [[True,False],
           [False,False]]

board2x2 = [[' ', ' '],
            ['1', ' ']]
            
grid3x3 = [[True ,False,False],
           [False,False,False],
           [False,False,True]]

board3x3 = [[' ', '1', '0'],
            [' ', '2', '1'],
            [' ', ' ', '*']]

board4x4 =  [[' ', '2', '2',' '],
               ['3', ' ', '3','2'],
               ['3', ' ', '5',' '],
               ['2', ' ', '4',' ']]

grid4x4 = [[True,False,False,True],
           [False,True,False,False],
           [False,True,False,True],
           [False,True,False,True]]

board4x3 =  [[' ', '2', '2',' '],
               ['3', ' ', '3','2'],
               ['3', ' ', '5',' ']
               ]

grid4x3 = [[True,False,False,True],
           [False,True,False,False],
           [False,True,False,True]
           ]
grid2x5 = [[False,False,True,True,True],
           [True,True,True,False,False]]

board2x5 = [[' ','4',' ',' ',' '],
            [' ',' ',' ','4','2']]


# game_lost(board) returns true if board contains one or more revealed mines,
#    false otherwise
# game_lost: GameBoard -> Bool
# Examples:
#    game_lost(board4x4) => False
#    game_lost(board4x3) => False

def game_lost(board):
    mined_rows = len(list(filter(lambda row: '*' in row, board)))
    return mined_rows != 0

# Tests:
check.expect("q4t1",game_lost(board4x4), False)
check.expect("q4t2",game_lost(board4x3), False)
check.expect("q4t3",game_lost(board3x3), True)

# count_mines(GorB,kind,n) consumes a MineGrid or MineBoard, GorB, a string
#     which is the unreavealed tile ' ' or the Bool that represents mine, True
#     and a natural number n. It returns the number of 'True' in the MineGrind 
#     or the number of '*' in the MineBoard.
# count_mines: (Anyof MineGrid MineBoard) Str Nat -> Nat
# Requires:
#     n = 0
#     kind = ' ' or '*'
# Examples:
#     count_mines(grid2x5,True,0) => 6
#     count_mines(board2x5,' ',0) => 7

def count_mines(GorB,kind,n):
    if n == len(GorB):
        return 0
    else:
        return len(list(filter(lambda a: a == kind, GorB[n]))) + \
               count_mines(GorB,kind,n+1)
    
# game_won(grid,board) consumes a MineGrid and a MineBoard.
#     These will represent the same game (so they will have the same dimensions 
#     and be consistent). The function returns True if the game has been won 
#     (all safe tiles are revealed, and no mine tiles are revealed), and False
#     otherwise.
# game_won: MineGrid MineBoard -> Bool
# Requires:
#     the length and width for grid and board should be same
# Examples:
#     game_won(grid4x4,board4x4) => True
#     game_won(grid3x3,board3x3) => False
    
def game_won(grid,board):
    if count_mines(grid,True,0) == count_mines(board,' ',0) \
       and len(list(filter(lambda row: '*' in row, board))) == 0:
        return True
    else:
        return False
    
# Tests:
check.expect("q4t4",game_won(grid3x3,board3x3), False)
check.expect("q4t5",game_won(grid4x3,board4x3), True)
check.expect("q4t6",game_won(grid4x4,board4x4), True)
check.expect("q4t7",game_won(grid2x2,board2x2), False)
check.expect("q4t8",game_won(grid2x5,board2x5), False)


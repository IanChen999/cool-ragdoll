##
##=======================================
## Yijun Chen (20739799)
## CS 116 Winter 2018
## Assignment 09
##=======================================
##

import check
import copy   

# Check the introduction of Kenken from www.kenken.com

class Puzzle:
    '''
    Fields:
            size: Nat 
            board: (listof (listof (anyof Str Nat Guess))
            constraints: (listof (list Str Nat (anyof '+' '-' '*' '/' '='))))
    requires: See Assignment Specifications
    '''
    
    def __init__(self, size, board, constraints):
        self.size=size
        self.board=board
        self.constraints=constraints
        
    def __eq__(self, other):
        return (isinstance(other,Puzzle)) and \
            self.size==other.size and \
            self.board == other.board and \
            self.constraints == other.constraints
    
    def __repr__(self):
        s='Puzzle(\nSize='+str(self.size)+'\n'+"Board:\n"
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.board[i][j],Guess):
                    s=s+str(self.board[i][j])+' '
                else:
                    s=s+str(self.board[i][j])+' '*7
            s=s+'\n'
        s=s+"Constraints:\n"
        for i in range(len(self.constraints)):
            s=s+'[ '+ self.constraints[i][0] + '  ' + \
                str(self.constraints[i][1]) + '  ' + self.constraints[i][2]+ \
                ' ]'+'\n'
        s=s+')'
        return s    

class Guess:
    '''
    Fields:
            symbol: Str 
            number: Nat
    requires: See Assignment Specifications
    '''        
    
    def __init__(self, symbol, number):
        self.symbol=symbol
        self.number=number
        
    def __repr__(self):
        return "('{0}',{1})".format(self.symbol, self.number)
    
    def __eq__(self, other):
        return (isinstance(other, Guess)) and \
            self.symbol==other.symbol and \
            self.number == other.number        

class Posn:
    '''
    Fields:
            y: Nat 
            y: Nat
    requires: See Assignment Specifications
    '''         
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)
    
    def __eq__(self,other):
        return (isinstance(other, Posn)) and \
            self.x==other.x and \
            self.y == other.y 
    
    

## Constants used for tests
    
puzzle1 = Puzzle(4, [['a','b','b','c'],
                     ['a','d','e','e'],
                     ['f','d','g','g'],
                     ['f','h','i','i']],
                 [['a', 6,'*'],
                  ['b',3,'-'],
                  ['c',3,'='],
                  ['d',5,'+'],
                  ['e',3,'-'],
                  ['f',3, '-'],
                  ['g',2,'/'],
                  ['h',4,'='],
                  ['i',1,'-']])

puzzle1partial=Puzzle(4, [['a','b','b','c'],
                          ['a',2,1,4],
                          ['f',3,'g','g'],
                          ['f','h','i','i']],
                      [['a', 6,'*'],
                       ['b',3,'-'],
                       ['c',3,'='],
                       ['f',3, '-'],
                       ['g',2,'/'],
                       ['h',4,'='],
                       ['i',1,'-']])

# a partial solution to puzzle1 with a cage partially filled in
puzzle1partial2=Puzzle(4, [[Guess('a',2),'b','b','c'],
                          ['a',2,1,4],
                          ['f',3,'g','g'],
                          ['f','h','i','i']],
                      [['a', 6,'*'],
                       ['b',3,'-'],
                       ['c',3,'='],
                       ['f',3, '-'],
                       ['g',2,'/'],
                       ['h',4,'='],
                       ['i',1,'-']])

# a partial solution to puzzle1 with a cage partially filled in
#   but not yet verified 
puzzle1partial3=Puzzle(4, [[Guess('a',2),'b','b','c'],
                          [Guess('a',3),2,1,4],
                          ['f',3,'g','g'],
                          ['f','h','i','i']],
                      [['a', 6,'*'],
                       ['b',3,'-'],
                       ['c',3,'='],
                       ['f',3, '-'],
                       ['g',2,'/'],
                       ['h',4,'='],
                       ['i',1,'-']])

# The solution to puzzle 1
puzzle1soln=Puzzle(4, [[2,1,4,3],[3,2,1,4],[4,3,2,1],[1,4,3,2]], [])

puzzle2=Puzzle(6,[['a','b','b','c','d','d'],
                  ['a','e','e','c','f','d'],
                  ['h','h','i','i','f','d'],
                  ['h','h','j','k','l','l'],
                  ['m','m','j','k','k','g'],
                  ['o','o','o','p','p','g']],
               [['a',11,'+'],
                ['b',2,'/'],
                ['c',20,'*'],
                ['d',6,'*'],
                ['e',3,'-'],
                ['f',3,'/'],
                ['g',9,'+'],
                ['h',240,'*'],
                ['i',6,'*'],
                ['j',6,'*'],
                ['k',7,'+'],
                ['l',30,'*'],
                ['m',6,'*'],
                ['o',8,'+'],
                ['p',2,'/']])
                
#  The solution to puzzle 2
puzzle2soln=Puzzle(6,[[5,6,3,4,1,2],
                      [6,1,4,5,2,3],
                      [4,5,2,3,6,1],
                      [3,4,1,2,5,6],
                      [2,3,6,1,4,5],
                      [1,2,5,6,3,4]], [])


puzzle3=Puzzle(2,[['a','b'],['c','b']],[['b',3,'+'],
                                       ['c',2,'='],
                                       ['a',1,'=']])

puzzle3partial=Puzzle(2,[['a',Guess('b',1)],['c',Guess('b',2)]],
                      [['b',3,'+'],
                       ['c',2,'='],
                       ['a',1,'=']])
                  
puzzle3soln=Puzzle(2,[[1,2],[2,1]],[])                  
                  
# part a)
## read_puzzle(fname) reads information from fname file and returns the info as 
## Puzzle value.
## read_puzzle: Str -> Puzzle

def read_puzzle(fname):
    file = open(fname,"r")
    List = file.readlines()
    rest = list(map(lambda x: x.strip().split(),List[1:]))
    size = int(List[0].strip())
    Board = list(filter(lambda x:len(x) == size,rest))
    Constraints = list(filter(lambda y:len(y) == 3,rest))
    for x in range(len(Constraints)):
        for y in range(3):
            if Constraints [x][y].isnumeric() == True:
                Constraints[x][y] = int( Constraints[x][y])
    file.close()
    return Puzzle(size,Board,Constraints)

check.expect("ta1", read_puzzle("inp1.txt"), puzzle1 )  


#part b)
## print_sol(puz, fname) prints the Puzzle puz in fname file
## print_sol: Puzzle Str -> Non

def print_sol(puz, fname):
    open_puz = open(fname,"w")
    puz_list = puz.board
    for x in range(len(puz_list)):
        open_puz.write('  '.join(str(y) for y in puz.board[x]) + \
                       '  \n')
    open_puz.close()
    
check.expect("Ta2", print_sol(puzzle1soln, "out1.txt"), None)
check.set_file_exact("out1.txt", "result.txt")

#part c)
## find_blank(puz) returns the position of the first blank
## space in puz, or False if no cells are blank.  If the first constraint has
## only guesses on the board, find_blank returns 'guess'.  
## find_blank: Puzzle -> (anyof Posn False 'guess')
## Examples:
## find_blank(puzzle1) => Posn(0 0)
## find_blank(puzzle3partial) => 'guess'
## find_blank(puzzle2soln) => False

def find_blank(puz):
    puz_list = puz.constraints
    if puz_list == []:
        return False
    else:
        for m in range(puz.size):
            for n in range(puz.size):
                if puz.board[m][n] == puz_list[0][0]:
                    return Posn(n,m)
        else:
            return 'guess'
            

check.expect("Tc1", find_blank(puzzle1),Posn(0,0))
check.expect("Tc2", find_blank(puzzle3partial),'guess')
check.expect("Tc3", find_blank(puzzle2soln),False)
check.expect("Tc4", find_blank(Puzzle(3, [["b","c","a"],["a","a","a"],
                                          ["d","a","e"]],
                                          [["a",18,"*"],["b",1,"="],["c",2,"="],
                                           ["d",3,"="],["e",1,"="]])), 
             Posn(2,0))
check.expect("Tc5",find_blank(Puzzle(3, 
                                     [[1,2,"d"],[Guess("b",2),3,Guess("b",1)],
                                      [Guess("b",3),Guess("b",1),Guess("b",2)]],
                                     [["b",12,"*"],["d",3,"="]])), 'guess')
#part d)
## used_in_row(puz, pos) returns a list of numbers used in the same 
## row as (x,y) position, pos, in the given puz.  
## used_in_row: Puzzle Posn -> (listof Nat)
## Example: 
## used_in_row(puzzle1,Posn(1,1)) => []
## used_in_row(puzzle1partial2,Posn(0,1)) => [1,2,4]

def used_in_row(puz,pos):
    puz_list = puz.board
    x = 0
    List = []
    while x < puz.size:
        if isinstance(puz_list[pos.y][x],int):
            List = List +[puz_list[pos.y][x]]
            x = x + 1
        else:
            x = x + 1
    return sorted(List)

check.expect("Td1", used_in_row(puzzle1,Posn(1,1)), [])
check.expect("Td2", used_in_row(puzzle1partial2,Posn(0,1)), [1,2,4])
check.expect("Td3", used_in_row(Puzzle(3,[[1,2,'d'],['b',3,'b'],
                                          ['b','b','b']],
                                       [['b',12,'*'],['d',3,'=']])
                                       ,Posn(0,1)), [3])

## used_in_col(puz, pos) returns a list of numbers used in the same 
## column as (x,y) position, pos, in the given puz.  
## used_in_col: Puzzle Posn -> (listof Nat)
## Examples:
## used_in_col(puzzle1partial2,Posn(1,0)) => [2,3]
## used_in_col(puzzle2soln,Posn(3,5)) => [1,2,3,4,5,6]

def used_in_col(puz,pos):
    puz_list = puz.board
    n = 0
    List = []
    while n < puz.size:
        if isinstance(puz_list[n][pos.x],int):
            List = List + [puz_list[n][pos.x]]
            n = n + 1
        else:
            n = n + 1
    return sorted(List)
    
    
check.expect("Td4", used_in_col(puzzle1partial2,Posn(1,0)), [2,3])  
check.expect("Td5", used_in_col(puzzle2soln,Posn(3,5)), [1,2,3,4,5,6])

#part e)
##available_vals(puz,pos) returns a list of valid entries for the (x,y)  
## position, pos, of the consumed puzzle, puz.  
## available_vals: Puzzle Posn -> (listof Nat)
## Examples:
## available_vals(puzzle1partial, Posn(2,2)) => [2,4]
## available_vals(puzzle1partial2, Posn(0,1)) => [3]

def available_vals(puz,pos):
    puz_list = []
    x = 1
    while x < puz.size + 1:
        puz_list = puz_list + [x]
        x = x + 1
    List = sorted(used_in_col(puz,pos) + used_in_row(puz,pos))
    return list(filter(lambda m: m not in List, puz_list))


check.expect("Te1", available_vals(puzzle1partial, Posn(2,2)), [2,4])
check.expect("Te2", available_vals(puzzle1partial2, Posn(0,1)), [3])

# part f)  
## place_guess(brd,pos,val) fills in the (x,y) position, pos, of the board, brd, 
## with the a guess with value, val
## place_guess: (listof (listof (anyof Str Nat Guess))) Posn Nat 
##              -> (listof (listof (anyof Str Nat Guess)))
## Examples:
## See provided tests

def place_guess(brd,pos,val):
    res=copy.deepcopy(brd)
    res[pos.y][pos.x] = Guess(res[pos.y][pos.x],val)
    return res


check.expect("Tf1", place_guess(puzzle3.board, Posn(1,1),2), 
             [['a','b'],['c',Guess('b',2)]])
check.expect("Tf2", place_guess(puzzle1partial2.board, Posn(0,1),3), 
             puzzle1partial3.board)


#  **********  DO NOT CHANGE THIS FUNCTION ******************

# fill_in_guess(puz, pos, val) fills in the pos Position of puz's board with 
# a guess with value val
# fill_in_guess: Puzzle Posn Nat -> Puzzle
# Examples: See provided tests

def fill_in_guess(puz,pos,val):
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    tmp=copy.deepcopy(res.board)
    res.board=place_guess(tmp, pos, val)
    return res


check.expect("Tf3", fill_in_guess(puzzle1, Posn(3,2),5), 
             Puzzle(4,[['a','b','b','c'], 
                      ['a','d','e','e'],
                      ['f','d','g',Guess('g',5)],
                      ['f','h','i','i']], puzzle1.constraints))


#  *************************************************************************             

# part g)
## guess_valid(puz) determines if the guesses in puz satisfy their constraint
## guess_valid: Puzzle -> Bool
## Examples: See provided tests

def guess_valid(puz):
    puz_list = []
    for a in range(puz.size):
        for b in range(puz.size):
            if isinstance(puz.board[a][b],Guess) and \
               puz.board[a][b].symbol == puz.constraints[0][0]:
                puz_list = puz_list + [puz.board[a][b].number]
    puz_list.sort()
    if puz.constraints[0][2] == '+' and \
       sum(puz_list) == puz.constraints[0][1] and \
       puz_list != []:
            return True
    elif puz.constraints[0][2] == '-' and \
         puz_list != []:
        if puz_list[0] - puz_list[1] == puz.constraints[0][1] or \
           puz_list[1] - puz_list[0] == puz.constraints[0][1]:
            return True
    elif puz.constraints[0][2] == '=' and \
         puz_list[0] == puz.constraints[0][1] and \
         puz_list != []:
        return True
    elif puz.constraints[0][2] == '*' and \
         puz_list != [] :
        c = 1
        for i in puz_list:
            c = c * i 
        if c == puz.constraints[0][1]:
            return True
    elif puz.constraints[0][2] == '/' and \
         puz_list != []:
        if puz_list[0] / puz_list[1] == puz.constraints[0][1] or \
           puz_list[1] / puz_list[0] == puz.constraints[0][1]:
            return True
    else: 
        return False
        
check.expect("Tg1", guess_valid(puzzle3partial), True)
check.expect("Tg2", guess_valid(Puzzle(3,[['a','a',3],
                                          ['a',Guess('b',1),2],
                                          ['a',Guess('b',3),1]],
                                       [['b',3,'/'],['a',8,'+']])), True)
check.expect("Tg3", guess_valid(Puzzle(2,[[Guess('a',2),Guess('a',1)],
                                          [Guess('a',1),Guess('a',2)]],
                                       [['a',4,'+']])), False)                                                      

# part h) 
## apply_guess(puz) converts all guesses in puz into their corresponding numbers
## and removes the first contraint from puz's list of contraints
## apply_guess:  Puzzle -> Puzzle
## Examples: See provided tests

def apply_guess(puz):
    # a copy of puz is assigned to res without any 
    # aliasing to avoid mutation of puz. 
    #  You should update res and return it    
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    for m in range(puz.size):
        for n in range(puz.size):
            if isinstance(res.board[m][n],Guess):
                res.board[m][n] = res.board[m][n].number
    res.constraints.pop(0)                    
    return res
                            
check.expect("Th1", apply_guess(Puzzle(6,[[5,6,3,4,1,2],[6,1,4,5,2,3],
                                          [4,5,2,3,6,1],[3,4,1,2,5,6],
                                          [2,3,6,1,4,5],
                                          [1,2,5,Guess('p',6),Guess('p',3),4]],
                                       [['p',2,'/']])), puzzle2soln)

# part i)
## neighbours(puz) returns a list of next puzzles after puz in
## the implicit graph
## neighbours: Puzzle -> (listof Puzzle)
## Examples: See provided tests

def neighbours(puz):
    # a copy of puz is assigned to tmp without any 
    # aliasing to avoid mutation of puz. 
    tmp=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    puz_list = []
    if find_blank(puz) == False:
        return []
    elif find_blank(puz) == 'guess':
        if guess_valid(puz):
            return [apply_guess(tmp)]
    elif find_blank(puz) != 'guess':
        for x in range(len(available_vals(tmp,find_blank(puz)))):
            puz_list = puz_list\
                + [fill_in_guess(tmp,find_blank(puz),\
                                 available_vals(tmp,find_blank(puz))[x])]
    return puz_list
   


check.expect("Ti1", neighbours(puzzle2soln), [])
check.expect("Ti2", neighbours(puzzle3), [Puzzle(2,[['a',Guess('b',1)],
                                                    ['c','b']],
                                                 [['b',3,'+'], ['c',2,'='],
                                                  ['a',1,'=']]),
                                          Puzzle(2,[['a',Guess('b',2)],
                                                    ['c','b']],[['b',3,'+'],
                                                                ['c',2,'='],
                                                                ['a',1,'=']])])
puz1=Puzzle(4,[[4,2,'a','a'],['b', Guess('c',3),'a',4],
               ['b', Guess('c',1),Guess('c',4),2],
               [1,Guess('c',4),Guess('c',2),3]],
            [['c',96,'*'],['b',5,'+'],['a',3,'*']])

puz2=Puzzle(4,[[4,2,'a','a'],['b',3,'a',4],['b',1,4,2],
               [1,4,2,3]],[['b',5,'+'],['a',3,'*']])
check.expect("Ti3",neighbours(puz1),[puz2])


# ******** DO NOT CHANGE THIS PART ***************
# ************** THE MAIN FUNCTION ***************
## solve_kenken(orig) finds the solution to a KenKen puzzle,
## orig, or returns False if there is no solution.  
## solve-kenken: Puzzle -> (anyof Puzzle False)
## Examples: See provided tests

def solve_kenken(orig):
    to_visit=[]
    visited=[]
    to_visit.append(orig)
    while to_visit!=[] :
        if find_blank(to_visit[0])==False:
            return to_visit[0]
        elif to_visit[0] in visited:
            to_visit.pop(0)
        else:
            nbrs = neighbours(to_visit[0])
            new = list(filter(lambda x: x not in visited, nbrs))
            new_to_visit=new + to_visit[1:] 
            new_visited= [to_visit[0]] + visited
            to_visit=new_to_visit
            visited=new_visited     
    return False


check.expect("game1",solve_kenken(puzzle3partial),False)
check.expect("game2",solve_kenken(puzzle1), puzzle1soln)
check.expect("game3",solve_kenken(puzzle2), puzzle2soln)
check.expect("game4",solve_kenken(puzzle3), puzzle3soln)
check.expect("game5",solve_kenken(puzzle3soln), puzzle3soln)
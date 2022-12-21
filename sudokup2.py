import sys
import time 
import math
import random


def nthRow(n):
    rowSet = set()
    for x in range (n*9,n*9+9):
        rowSet.add(x)
    return rowSet

def nthColumn(n):
    columnSet = set()
    for x in range (n,n+81,9):
        columnSet.add(x)
    return columnSet

def nthSquare(n):
    squareSet = set()
    addiplier = n % 3
    multiplier = 0
    if n > 2:
        multiplier = 1
    if n > 5:
        multiplier = 2
    start = addiplier*3 + multiplier*27
    for i in range (0,27,9):
        for j in range (start+i,start+i+3):
            squareSet.add(j)
    return squareSet

constraints = []
for x in range (0,9):
    constraints.append(nthRow(x))
    constraints.append(nthColumn(x))
    constraints.append(nthSquare(x))

squareCons = {}
for i in range (0,81):
    row = i // 9
    column = i % 9
    square = 0 
    if column < 3:
        square = 0
    if column < 6 and column > 2:
        square = 1
    if column > 5:
        square = 2
    if row < 6 and row > 2:
        square = square + 3 
    if row > 5:
        square = square + 6 
    fullset = nthRow(row) | nthColumn(column) | nthSquare(square)
    fullset.remove(i) 
    squareCons[i] = fullset

case = sys.argv[1]

def read():
    with open(case) as f:
        line_list = [line.strip() for line in f]
    return line_list

def forwardlook(state,var):
    for i in var:
        for x in squareCons[i]:
            if state[i][0] in state[x]:
                state[x].remove(state[i][0])
                if len(state[x]) == 1:
                    var.append(x)
                if len(state[x]) == 0:
                    return None
    return state

def createBoard(state):
    board = []
    forward = []
    for i, num in enumerate(state):
        if num == ".":
            board.append(["1","2","3","4","5","6","7","8","9"])
        else:
            board.append([num])
            forward.append(i)
    return forwardlook(board,forward)

boards = []
for i in read():
    boards.append(createBoard(i))

def boardPrint(board):
    ind = 0 
    s = ""
    for i in range (0,9):
        for j in range (0,9):
            s = s + board[ind] + " "
            ind = ind + 1
        s = s + "\n"
    print(s)

def get_mostconstrained(state):
    min = 9
    ind = [] 
    for i in range (0,len(state)):
        if len(state[i]) != 1 and len(state[i]) <= min:
            min = len(state[i])
            ind.append(i)
    ran = [] 
    for j in ind:
        if len(state[j]) == min:
            ran.append(j)
    if len(ran) == 1:
        return ran[0]
    return random.choice(ran)

symbols = [".","1","2","3","4","5","6","7","8","9"]

def symbolcount (state):
    count = {}
    for x in symbols:
        count[x] = 0 
    for x in range (0,len(state)):
        count[state[x]] = count.get(state[x]) + 1
    return count 

def get_sorted(state,var):
    return state[var]

def assign(state,var,val):
    state[var] = [val]
    return state

def goal(state):
    bool = True
    for i in state:
        if len(i) != 1:
            bool = False
    return bool

def csp_backtracking_forwardlooking(puzz):
    if goal(puzz):
        s = ""
        for x in puzz:
            s = s + x[0]
        return s
    var = get_mostconstrained(puzz)
    for val in get_sorted(puzz,var):
        new_board = [x.copy() for x in puzz]
        checked_board = forwardlook(assign(new_board,var,val),[var])
        if checked_board is not None:
            result = csp_backtracking_forwardlooking(checked_board)
            if result is not None:
                return result
    return None

for i in boards:
    print(csp_backtracking_forwardlooking(i))
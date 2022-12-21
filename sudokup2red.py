import sys
from tabnanny import check
import time 
import math
import random
from venv import create


def nthRow(n,height,length):
    rowSet = set()
    for x in range (n*height,n*height+length):
        rowSet.add(x)
    return rowSet

def nthColumn(n,height,length):
    columnSet = set()
    for x in range (n,n+height*length,length):
        columnSet.add(x)
    return columnSet

def nthSquare(n,height,length):
    squareSet = set()
    rt = math.sqrt(height)
    width = math.ceil(rt)
    while height % width != 0:
        width = width + 1 
    side = math.floor(rt)
    while height % side != 0:
        side = side - 1 
    addiplier = n % (height/width)
    multiplier = 0
    row = int(height/width)
    while n >= row:
        multiplier = multiplier + 1 
        row = int(row + height/width)
    start = int(addiplier*width + multiplier*(height/width)*width*side)
    for i in range (0,height*side,length):
        for j in range (start+i,start+i+width):
            squareSet.add(j)
    return squareSet


def createConstraints(height,length):
    constraints = []
    for x in range (0,height):
        constraints.append(nthRow(x,height,length))
    for x in range(0,length):
        constraints.append(nthColumn(x,height,length))
    for x in range (0,height):
        constraints.append(nthSquare(x,height,length))
    return constraints 

def createSquareCons(height,length):
    squareCons = {}
    for i in range (0,height*length):
        row = i // height
        column = i % length

        rt = math.sqrt(height)
        width = math.ceil(rt)
        while height % width != 0:
            width = width + 1 
        side = math.floor(rt)
        while height % side != 0:
            side = side - 1 

        square = int(column // width + (row//side) * (height/width))

        fullset = nthRow(row,height,length) | nthColumn(column,height,length) | nthSquare(square,height,length)
        fullset.remove(i) 
        squareCons[i] = fullset

    return squareCons

case = sys.argv[1]

def read():
    with open(case) as f:
        line_list = [line.strip() for line in f]
    return line_list

boards = read()

def boardPrint(board,height,length):
    ind = 0 
    s = ""
    for i in range (0,length):
        for j in range (0,length):
            s = s + board[ind] + " "
            ind = ind + 1
        s = s + "\n"
    print(s)

def forwardlook(state,var,squareCons):
    for i in var:
        for x in squareCons[i]:
            if state[i][0] in state[x]:
                state[x].remove(state[i][0])
                if len(state[x]) == 1:
                    var.append(x)
                if len(state[x]) == 0:
                    return None
    return state

def createOptions(height):
    options = []
    if height < 10:
        for i in range (1,height+1):
            options.append(str(i))
    else:
        letters = ["A","B","C","D","E","F","G"]
        for i in range (1,10):
            options.append(str(i))
        for j in range (10,height+1):
            options.append(letters[j-10])
    return options

def createBoard(state,squareCons):
    board = []
    forward = []
    height = int(math.sqrt(len(state)))
    options = createOptions(height)
    for i, num in enumerate(state):
        if num == ".":
            board.append(options.copy())
        else:
            board.append([num])
            forward.append(i)
    return forwardlook(board,forward,squareCons)

boards = []
for i in read():
    height = int(math.sqrt(len(i)))
    length = height 
    squareCons = createSquareCons(height,length)
    options = createOptions(height)
    boards.append((createBoard(i,squareCons),squareCons,options,height))


def get_mostconstrained(state,height,length):
    min = height
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

def createConSet(height,length):
    conSet = []
    for i in range(0,height):
        conSet.append(nthRow(i,height,length))
        conSet.append(nthColumn(i,height,length))
        conSet.append(nthSquare(i,height,length))
    return conSet 

def constraintSat(state,height,length,constraintSet,options,sqCon):
    ls = [] 
    for i in constraintSet:
        for j in options:
            count = 0 
            for k in i:
                if j in state[k]:
                    count = count + 1
                    ind = k 
            if count == 1:
                state[ind] = [j]
                ls.append(ind)
    return forwardlook(state,ls,sqCon)


def checkFailure(state,height):
    for i in createConSet(height,height):
        ls = [] 
        for j in i:
            if len(state[j]) == 1: 
                if state[j][0] in ls:
                    return('here')
                ls.append(state[j][0])
    return ('good')

# symbols = [".","1","2","3","4","5","6","7","8","9"]

# def symbolcount (state):
#     count = {}
#     for x in symbols:
#         count[x] = 0 
#     for x in range (0,len(state)):
#         count[state[x]] = count.get(state[x]) + 1
#     return count 

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

def csp_backtracking_forwardlooking(puzz,squareCons,options,height,length,conSet):
    if goal(puzz):
        s = ""
        for x in puzz:
            s = s + x[0]
        return s
    var = get_mostconstrained(puzz,height,length)
    for val in get_sorted(puzz,var):
        new_board = [x.copy() for x in puzz]
        checked_board = forwardlook(assign(new_board,var,val),[var],squareCons)
        if checked_board is not None: 
            the_board = constraintSat(checked_board,height,length,conSet,options,squareCons)
            if the_board is not None:
                result = csp_backtracking_forwardlooking(the_board,squareCons,options,height,length,conSet)
                if result is not None:
                    return result
    return None

for i,squareCons,options,height in boards:
    conSet = createConSet(height,height)
    length = height 
    board = csp_backtracking_forwardlooking(i,squareCons,options,height,length,conSet)
    print(board)
    #print(checkFailure(board,height))
    
    
import sys
import time 
import math



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

def get_nextun(board):
    ind = 0
    while board[ind] != ".":
        ind = ind + 1
    return ind 

def createSymbols(height,length):
    symbols = ["."]
    for i in height:
        symbols.append(str(i))
    return symbols 


def symbolcount(state,height,length):
    count = {}
    symbols = createSymbols(height,length)
    for x in symbols:
        count[x] = 0 
    for x in range (0,len(state)):
        count[state[x]] = count.get(state[x]) + 1
    return count 

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

def get_sorted(state,var,squareCons,options):
    remove = []
    newoptions = options.copy()
    for i in newoptions:
        for j in squareCons[var]:
            if i == state[j]:
                if i not in remove:
                    remove.append(i)
    for x in remove:                
        newoptions.remove(x)
    return newoptions 


def csp_backtracking(puzz,squareCons,options):
    if "." not in puzz:
        return puzz
    var = get_nextun(puzz)
    for val in get_sorted(puzz,var,squareCons,options):
        newstring = puzz[0:var] + val + puzz[(var+1):]
        result = csp_backtracking(newstring,squareCons,options)
        if result is not None:
            return result
    return None

for i in boards:
    height = int(math.sqrt(len(i)))
    length = height 
    squareCons = createSquareCons(height,length)
    options = createOptions(height)
    print(csp_backtracking(i,squareCons,options))

import sys
import time 


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

print(nthSquare(3))

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
print(squareCons)

case = sys.argv[1]

def read():
    with open(case) as f:
        line_list = [line.strip() for line in f]
    return line_list

boards = read()

def boardPrint(board):
    ind = 0 
    s = ""
    for i in range (0,9):
        for j in range (0,9):
            s = s + board[ind] + " "
            ind = ind + 1
        s = s + "\n"
    print(s)

def get_nextun(board):
    ind = 0
    while board[ind] != ".":
        ind = ind + 1
    return ind 

symbols = [".","1","2","3","4","5","6","7","8","9"]

def symbolcount (state):
    count = {}
    for x in symbols:
        count[x] = 0 
    for x in range (0,len(state)):
        count[state[x]] = count.get(state[x]) + 1
    return count 

def get_sorted(state,var):
    options = ["1","2","3","4","5","6","7","8","9"]
    remove = []
    for i in options:
        for j in squareCons[var]:
            if i == state[j]:
                if i not in remove:
                    remove.append(i)
    for x in remove:                
        options.remove(x)
    return options 


def csp_backtracking(puzz):
    if "." not in puzz:
        return puzz
    var = get_nextun(puzz)
    for val in get_sorted(puzz,var):
        newstring = puzz[0:var] + val + puzz[(var+1):]
        result = csp_backtracking(newstring)
        if result is not None:
            return result
    return None

# for i in boards:
#     print(csp_backtracking(i))
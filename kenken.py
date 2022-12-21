import sys
import time 
import math
import random
from venv import create

case = sys.argv[1]

def read():
    with open(case) as f:
        line_list = [line.strip() for line in f]
    return line_list

input = read()

board = input[0]
length = int(math.sqrt(len(board)))

def boardPrint(board):
    ind = 0 
    s = ""
    for i in range (0,length):
        for j in range (0,length):
            s = s + board[ind] + " "
            ind = ind + 1
        s = s + "\n"
    print(s)

def createBlocks(input):
    blocks = {}
    for i in range (1,len(input)):
        line = input[i].split(" ")
        blocks[line[0]] = (line[1],line[2])
    return blocks 

blocks = createBlocks(input)

def nthRow(n,length):
    rowSet = set()
    for x in range (n*length,n*length+length):
        rowSet.add(x)
    return rowSet

def nthColumn(n,length):
    columnSet = set()
    for x in range (n,n+length*length,length):
        columnSet.add(x)
    return columnSet

def createRowColCons(length):
    cons = {}
    for i in range (0,length*length):
        row = i // length
        column = i % length

        fullset = nthRow(row,length) | nthColumn(column,length)
        fullset.remove(i) 
        cons[i] = fullset
    return cons 

rowColCons = createRowColCons(length)

def createBoxes():
    boxes = {}
    for i in blocks:
        indices = [] 
        hold = 0
        while i in board[hold:]:
            ind = board[hold:].find(i) + hold 
            indices.append(ind)
            hold = ind+1
        boxes[i] = indices
    return boxes

boxes = createBoxes()

def createOptions(length):
    options = []
    for i in range (1,length+1):
        options.append(i)
    return options

options = createOptions(length)

def createState(length):
    state = ""
    for i in range (0,length*length):
        state = state + "."
    return state

state = createState(length)

def doOperation(nums,operation,goal):
    sum = 0 
    if operation == "+":
        for i in nums:
            sum = sum + i
    elif operation == "-":
        sum = nums[1] - nums[0] 
        if sum == goal:
            return sum
        sum = nums[0] - nums[1]
        if sum == goal:
            return sum 
    elif operation == "x":
        sum = nums[0]
        for i in range (1,len(nums)):
            sum = sum * nums[i]
    elif operation == "/":
        sum = nums[1] / nums[0] 
        if sum == goal:
            return sum
        sum = nums[0] / nums[1]
        if sum == goal:
            return sum
    return sum 

def isValid(state,var,val):
    goal, operation = blocks.get(board[var])
    nums = [int(val)]
    for i in boxes.get(board[var]):
        if i != var:
            if state[i] != ".":
                nums.append(int(state[i]))
    if len(nums) == len(boxes.get(board[var])):
        sum = int(doOperation(nums,operation,int(goal)))
        if sum == int(goal):
            return True
        else:
            return False
    return True

def get_nextun(state):
    ind = 0
    while state[ind] != ".":
        ind = ind + 1
    return ind

def get_sorted(state,var):
    remove = []
    newoptions = options.copy()
    for i in newoptions:
        for j in rowColCons.get(var):
            if state[j] != ".":
                k = int(state[j])
                if i == k:
                    if i not in remove:
                        remove.append(i)
    for x in remove:                
        newoptions.remove(x)
    realoptions = [] 
    for i in newoptions:
        if isValid(state,var,i):
            realoptions.append(i)
    return realoptions

def csp_backtracking(puzz):
    if "." not in puzz:
        return puzz
    var = get_nextun(puzz)
    for val in get_sorted(puzz,var):
        newstring = puzz[0:var] + str(val) + puzz[(var+1):]
        result = csp_backtracking(newstring)
        if result is not None:
            return result
    return None



boardPrint(csp_backtracking(state))
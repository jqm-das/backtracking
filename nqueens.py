import sys
import time
import math 
import random


def boardCreate(thesize):
    board = []
    for i in range(0,thesize):
        board.append(-1)
    return board

def get_nextun(state):
    i = 0
    while state[i] != -1:
        i = i + 1
    return i

def get_sorted(state,var,size):
    sorted = []
    for j in range (0,size):
        bool = True
        for k in range (0,var):
            if j == state[k] or abs((j-state[k])/(var-k)) == 1:
                bool = False
        if bool:
            sorted.append(j)
    return sorted

def goal(state):
    for j in state:
        if j == -1:
            return False
    return True

def csp_backtracking(state):
    if goal(state):
        return state
    var = get_nextun(state)
    for val in get_sorted(state,var):
        state[var] = val
        newlist = state.copy()
        result = csp_backtracking(newlist)
        if result is not None:
            return result
    return None

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

def get_nextunimproved(state,size):
    i = size//2
    j = i
    k = i 
    while state[j] != -1:
        j = j + 1
        if j > size-1:
            break
    while state[k] != -1:
        k = k - 1
        if k < 0:
            break
    if j - i < i - k or j == size:
        return k
    return j
    
def createKey(size):
    ls = []
    while len(ls) != size:
        i = random.randint(0,size-1)
        while i in ls:
            i = random.randint(0,size-1)
        ls.append(i)
    return ls

def sort(size):
    ls = []
    j = size//2 - 1
    k = size//2 
    if size % 2 == 0:
        while len(ls) != size:
            ls.append(j)
            ls.append(k)
            j = j - 1
            k = k + 1
    else: 
        while len(ls) != size-1:
            ls.append(k)
            ls.append(j)
            j = j - 1
            k = k + 1
        ls.append(k)
    return ls


def get_sortedimproved(state,var,size):
    sorted = []
    for j in order:
        bool = True
        for k in range (0,size):
            if state[k] != -1:
                if j == state[k] or abs((j-state[k])/(var-k)) == 1:
                    bool = False
        if bool:
            sorted.append(j)
    return sorted

def csp_backtrackingimproved(state,size):
    if goal(state):
        return state
    var = get_nextunimproved(state,size)
    for val in get_sortedimproved(state,var,size):
        state[var] = val
        newlist = state.copy()
        result = csp_backtrackingimproved(newlist,size)
        if result is not None:
            return result
    return None

# start = time.perf_counter()
# order = createKey(31)
# board = boardCreate(31)
# s = csp_backtrackingimproved(board,31)
# print(str(s) + " Size: 31")
# print(test_solution(s))
# order = createKey(32)
# board = boardCreate(32)
# s = csp_backtrackingimproved(board,32)
# print(str(s) + " Size: 32")
# print(test_solution(s))
# end = time.perf_counter()
# print("Time Elapsed(backtrack): %s" % (end-start))

def generate(board,size):
    state = board
    while board[size-1] == -1:
        var = get_nextun(state)
        z = get_sortedimproved(state,var,size)
        if len(z) == 0:
            state[var] = size//2
        else:
            state[var] = z[0]
    return state

def findConflict(state,row,index,size):
    count = 0 
    for i in range (0,size):
        if i != row:
            if index == state[i] or abs((index-state[i])/(row-i)) == 1:
                count = count + 1
    return count 

def findAllConflict(state,size):
    count = 0 
    index = 0 
    max = 0 
    ls = [] 
    for i in range (0,size):
        rowcon = findConflict(state,i,state[i],size)
        count = count + rowcon
        if rowcon >= max:
            ls.append((rowcon,i))
            max = rowcon
    if len(ls) == 1:
        return count,i
    ran = [] 
    for j,k in ls:
        if j == max:
            ran.append(k)
    if len(ran) == 1:
        return count,ran[0]
    return count,ran[random.randint(0,(len(ran)-1))]

def findLeastConflict(state,row,size):
    index = 0
    min = findConflict(state,row,state[row],size)
    ls = []
    for i in range (0,size):
        temp = findConflict(state,row,i,size)
        if temp <= min:
            min = temp
            ls.append((temp,i))
    ran = []
    for j,k in ls:
        if j == min:
            ran.append(k)
    if len(ran) == 1:
        return ran[0]
    return ran[random.randint(0,(len(ran)-1))]


def incremental(state,size):
    x,y = findAllConflict(state,size)
    while x > 0:
        x,row = findAllConflict(state,size)
        index = findLeastConflict(state,row,size)
        state[row] = index 
        print(state)
        print("Num of Conflicts: %s" % x)
    return state

board = boardCreate(31)
order = createKey(31)
start = time.perf_counter()
s = generate(board,31)
k = incremental(s,31)
print("Size: 31")
print(k)
print(test_solution(s))
board = boardCreate(32)
order = createKey(32)
s = generate(board,32)
k = incremental(s,32)
print("Size 32:")
print(k)
print(test_solution(s))
end = time.perf_counter()
print("Time Elapsed(incremental): %s" % (end-start))
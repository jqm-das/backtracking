import sys

# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
puzzle = sys.argv[1].split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions

def area_check(rectangles):
    sum = 0 
    for rect in rectangles:
        a,b = rect
        sum = sum + a*b
    if sum == puzzle_width * puzzle_height:
        return True
    return False

def flip (rectangles,var):
    a,b = rectangles[var] 
    rectangles[var] = (b,a)
    return rectangles

def board_create(height,width):
    s = []
    for j in range (0,height*width):
        s.append("o")
    return s 

board = board_create(puzzle_height,puzzle_width)

def get_nextunassigned(state):
    ind = 0 
    while state[ind] != "o":
        ind = ind + 1
    return ind

def get_sorted(rect,state,var):
    options = [] 
    for height,width in rect:
        bool = True
        h = var // puzzle_height
        w = var % puzzle_height
        for i in range (h,h+height):
            for j in range (w, w+width):
                ind = i*puzzle_width+j
                if ind > len(state):
                    bool = False
                if ind < len(state):
                    if state[ind] == "x":
                        bool = False
        if bool:
            options.append((height,width))
        if height != width:
            bool = True
            for i in range (h,h+width):
                for j in range (w, w+height):
                    ind = i*puzzle_width+j
                    if ind > len(state):
                        bool = False
                    if ind < len(state):
                        if state[ind] == "x":
                            bool = False
            if bool:
                options.append((width,height))
    return options 

def assign(state,val,var):
    height,width = val
    h = var // puzzle_height
    w = var % puzzle_width
    for i in range (h,h+height):
        for j in range (w, w+width):
            ind = i*puzzle_width+j
            state[ind] = "x"
    return state

def goal(state):
    if "o" not in state:
        return True
    return False

def board_print(board):
    s = ""
    for i in range (0,puzzle_height):
        for j in range(0,puzzle_width):
            s = s + (board[i*puzzle_width+j])
        s = s + "\n"
    print(s)

def remove_rect(rect,val):
    if val not in rect:
        a,b = val
        rect.remove((b,a))
    else:
        rect.remove(val)
    return rect

def csp_backtracking(state,rect):
    if goal(state):
        return state
    var = get_nextunassigned(state)
    board_print(state)
    for val in get_sorted(rect,state,var):
        newstate = state.copy()
        newrect = remove_rect(rect.copy(),val)
        newstate = assign(newstate,val,var)
        result = csp_backtracking(newstate,newrect)
        if result is not None:
            return result
    return None

print(csp_backtracking(board,rectangles))

# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
#
# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.
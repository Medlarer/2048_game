#! /usr/bin/python


"""Just a test file"""


import random 
import sys


v = [[0, 0, 0, 0],
        [0, 0, 0, 0], 
        [0, 0, 0, 0],
        [0, 0, 0, 0] ]

def display(v, score):
    """UI
    """
    print "{0: 4} {1: 4} {2: 4} {3: 4}".format(v[0][0], v[0][1], v[0][2],
            v[0][3])
    print "{0: 4} {1: 4} {2: 4} {3: 4}".format(v[1][0], v[1][1], v[1][2],
            v[1][3])
    print "{0: 4} {1: 4} {2: 4} {3: 4}".format(v[2][0], v[2][1], v[2][2],
            v[2][3])
    print "{0: 4} {1: 4} {2: 4} {3: 4}".format(v[3][0], v[3][1], v[3][2],
            v[3][3]) 
    print "total_score: %d" % score


def init(v):
    """Randomly assign grid values
    """
    for i in range(4):
        v[i] = [random.choice([0, 0, 0, 2, 2, 4]) for x in v[i]]


def align(vList, direction):
    """Align non-zero numbers
    direction == "left": Align to the left, eg[8, 0, 0, 2] left aligned 
    [8, 2, 0, 0]
    direction == "right": Align to the right, eg[8, 0, 0, 2] right aligned
    [0, 0, 8, 2]"""
    
    for i in range(vList.count(0)):
        vList.remove(0)
    #Remove 0 from the list
    zeros = [0 for x in range(4 - len(vList))]
    if direction == "left":
        vList.extend(zeros)
    else:
        vList[: 0] = zeros


def add_same(vList, direction):
    """Find the same and adjacent numbers in the list, find the return
    condition taht matches the condition, otherwise return False, and also
    return the added score
    direction == "left": Find from right to left, find the same and adjacent
    two numbers, the left numbers is doubled, and the right numbers is set to 0
    direction == "right": Find from left to right, find the same and adjacent
    two numbers, double the number on the right, and set the number on the left
    to 0"""

    score = 0
    if direction == "left":
        for i in [0, 1, 2]:
            if vList[i] == vList[i+1] != 0:
                vList[i] *= 2
                vList[i+1] = 0
                score += vList[i]
                return {"bool": True, "score": score}
    else:
        for i in [3, 2, 1]:
            if vList[i] == vList[i-1] != 0:
                vList[i-1] *=2
                vList[i] = 0
                score += vList[i-1]
                return {"bool": True, "score": score}
    return {"bool": False, "score": score}

def handle(vList, direction):
    """Process the data in one row (column) to get the final numeric state
    value of the row (column), return the score
    vList: List structure
    direction: direction of movement
    """
    total_score = 0
    align(vList, direction)
    result = add_same(vList, direction)
    while result["bool"] == True:
        total_score += result["score"]
        align(vList, direction)
        result = add_same(vList, direction)
    return total_score


def operation(v):
    """Recalculate matrix sate values based on the direction of movement and
    record the score"""
    total_score = 0
    game_over = False
    direction = "left"
    op = raw_input("operator: ")
    if op in ["a", "A"]:
        direction = "left" #Move to the left
        for row in range(4):
            total_score += handle(v[row], direction)
    elif op in ["d", "D"]:
        direction = "right" #Move to the right
        for row in range(4):
            total_score += handle(v[row], direction)
    elif op in ["w", "W"]:
        direction = "left" #Move up
        for col in range(4):
            vList = [v[row][col] for row in range(4)]
            total_score += handle(vList, direction)
            for row in range(4):
                v[row][col] = vList[row]
    elif op in ["s", "S"]: #Move down
        direction = "right"
        for col in range(4):
            vList = [v[row][col] for row in range(4)]
            total_score += handle(vList, direction)
            for row in range(4):
                v[row][col] = vList[row]
    else:
        print("Invalid input, please enter a charactor in [W, S, A, D]")
        return {"game_over": game_over, "score": total_score}
    N = 0 # Count the number of the 0
    for q in v:
        N += q.count(0)
    if N == 0:
        game_over = True
        return {"game_over":game_over, "score": total_score}
    num = random.choice([2, 2, 2, 4])
    k = random.randrange(1, N+1)
    n = 0
    for i in range(4):
        for j in range(4):
            if v[i][j] == 0:
                n += 1
                if n == k:
                    v[i][j] = num 
                    break
    return {"game_over": game_over, "score": total_score}

init(v)
score = 0
print "Input: W(Up) S(Down) A(Left) D(Right), press <CR>."
while True:
    display(v, score)
    result = operation(v)
    if result["game_over"] == True:
        print "Game Over, You failed!"
        print "Your total score:", score
        sys.exit(1)
    else:
        score += result["score"]
        if score >= 2048:
            print "Game Over, You Win!!!"
            print "Your total score:", score
            sys.exit(0)

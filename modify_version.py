#!/usr/bin/python


"""Modify version
"""


import random
import os, sys


v = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0], 
     [0, 0, 0, 0]]


def display(v, score):
    print "%4d %4d %4d %4d" % (v[0][0], v[0][1], v[0][2], v[0][3])
    print "%4d %4d %4d %4d" % (v[1][0], v[1][1], v[1][2], v[1][3])
    print "%4d %4d %4d %4d" % (v[2][0], v[2][1], v[2][2], v[2][3])
    print "%4d %4d %4d %4d" % (v[3][0], v[3][1], v[3][2], v[3][3])
    print "Total score: %d" % score


def init(v):
    for i in range(4):
        v[i] = [random.choice([0, 0, 0, 2, 2, 4]) for x in range(4)]


def align(vList, direction):
    for i in range(vList.count(0)):
        vList.remove(0)
    zeros = [0 for x in range(4 - len(vList))]
    if direction == "left":
        vList.extend(zeros)
    else:
        vList[: 0] = zeros


def add_same(vList, direction):
    score = 0
    if direction == "left":
        for i in [0, 1, 2]:
            align(vList, direction)
            if vList[i] == vList[i+1] !=0:
                vList[i] *=2
                vList[i+1] = 0
                score += vList[i]
                return {"bool": True, "score": score}
    else:
        for i in [3, 2, 1]:
            align(vList, direction)
            if vList[i] == vList[i-1] != 0:
                vList[i] *= 2
                vList[i-1] = 0
                score += vList[i]
                return {"bool": True, "score": score}
    return {"bool": False, "score": score}


def handle(vList, direction):
    total_score = 0
    align(vList, direction)
    result = add_same(vList, direction)
    while result["bool"] == True:
        total_score += result["score"]
        align(vList, direction)
        result = add_same(vList, direction)
    return total_score


def operator(v):
    total_score = 0
    game_over = False
    direction = "left"
    op = raw_input("operator:")
    if op in ["a", "A"]:
        direction = "left"
        for row in range(4):
            total_score += handle(v[row], direction)
    elif op in ["d", "D"]:
        direction = "right"
        for row in range(4):
            total_score += handle(v[row], direction)
    elif op in ["w", "W"]:
        direction = "left"
        for col in range(4):
            vList = [v[row][col] for row in range(4)]
            total_score += handle(vList, direction)
            for row in range(4):
                v[row][col] = vList[row]
    elif op in ["s", "S"]:
        direction = "right"
        for col in range(4):
            vList = [v[row][col] for row in range(4)]
            total_score += handle(vList, direction)
            for row in range(4):
                v[row][col] = vList[row]
    else:
        print("Invalid input, please enter a charactor in [W, S, A, D]")
        game_over = True
        return {"game_over": game_over, "score":total_score}
    N = 0
    for q in v:
        N += q.count(0)

    if N == 0:
        game_over = True
        return {"game_over": game_over, "score": total_score}
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
    os.system("clear")
    display(v, score)
    result = operator(v)
    print result
    if result["game_over"] == True:
        print "Game Over, You Failed!"
        print "Your total score %d" % (score)
        sys.exit(1)
    else:
        score += result["score"]
        if score >= 2048:
            print "Game Over, Your Win!!!"
            print "Your total score: %d" % (score)
            sys.exit(0)



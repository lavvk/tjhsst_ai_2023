import sys
from collections import deque
from time import perf_counter
from heapq import heappush, heappop

def goal_test(string):
    return ''.join(sorted(string))[1:]+'.'

def parity(string):
    out_of_order = 0
    length = int(len(string)**(1/2))
    period = string.index('.')
    row = int(period/length)
    modified = string[:period] + string[period+1:]
    sort = "".join(sorted(modified))
    for i in range(len(sort)):
        period = modified.index(sort[i])
        for j in range(0, period+1):
            if modified[j] > sort[i]: 
                out_of_order += 1
    if length%2==0:
        if row%2==0:
            return out_of_order%2==1
        else:
            return out_of_order%2==0
    else:
        return out_of_order%2==0

def heuristic(string):
    moves = 0
    length = int(len(string) ** (1/2))
    sorted_string = "".join(sorted(string))[1:]
    
    for i in range(len(sorted_string)):
        correct_row = i // length
        correct_col = i % length
        
        current_index = string.index(sorted_string[i])
        
        moves += abs(current_index // length - correct_row) + abs(current_index % length - correct_col)
    
    return moves


def get_children(size, string): ## same from bfs
    children = []

    i = string.index('.')
    r, c = divmod(i, size)

    for m in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        row, col = r + m[0], c + m[1]
        if 0 <= row < size and 0 <= col < size:
            n = row * size + col
            child = list(string)
            child[i], child[n] = child[n], child[i]
            children.append(''.join(child))
    return children


def a_star(string):
    closed = set()
    fringe = []
    start_node = (heuristic(string), string, 0)
    heappush(fringe, start_node)
    length = int(len(string)**(0.5))

    while len(fringe)!=0:
        v = heappop(fringe)
        if v[1]==goal_test(string):
            return v[2]
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(length, v[1]):
                if child not in closed:
                    temp = (v[2]+1+heuristic(child), child, v[2]+1)
                    heappush(fringe, temp)
    return None

with open(sys.argv[1], "r") as f:
    line_list = [line.strip() for line in f]

for i, line in enumerate(line_list):
    start = perf_counter()
    temp = line.split()
    puzzle_number = temp[1]
    if parity(puzzle_number):
        status = "A* - " + str(a_star(puzzle_number)) + " moves found"
    else:
        status = "no solution determined"

    end = perf_counter()
    print("Line " + str(i) + ": " + puzzle_number + ", " + status + " in " + str(end - start) + " seconds")

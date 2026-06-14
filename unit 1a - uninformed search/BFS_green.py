import sys

from collections import deque
from time import perf_counter

def get_children(size, string):
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

def bfs(string):
    fringe = deque([[string, [string]]])
    visited = set([string])
    length = int(len(string) ** 0.5)

    goal_string = ''.join(sorted(string))[1:] + '.'

    while len(fringe) != 0:
        v = fringe.popleft()
        if v[0] == goal_string:
            return len(v[1]) - 1
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

with open("slide_puzzle_tests.txt", "r") as f:
    line_list = [line.strip() for line in f]

    for i, puzzle in enumerate(line_list):
        start_time = perf_counter()
        data = puzzle.split()
        puzzle_input = data[1]
        solution = bfs(puzzle_input)
        end_time = perf_counter()
        if solution is not None:
            print("Line " + str(i) + ": " + puzzle_input + ", " + str(solution) + " moves found in " + str(end_time - start_time) + " seconds")
        else:
            print("Line " + str(i) + ": " + puzzle_input + " No solution found")


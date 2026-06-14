from collections import deque
from time import perf_counter
import sys


def get_children(size, string): ## same as othe lab lolz
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

def bfs(string, goal): ## kindaaaa same as old one edit gosl stuff
    fringe = deque([[string, [string]]])
    visited = set([string])
    length = int(len(string)**(1/2))
    
    while len(fringe) != 0:
        v = fringe.popleft()
        if v[0] == goal:
            return len(v[1]) - 1
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

def kdfs(string, k, goal, length):
    fringe = []
    start_node = (string, 0, {string})
    fringe.append(start_node)
    while len(fringe) != 0:
        v = fringe.pop()
        if v[0] == goal:
            return v[1]
        if v[1] < k:
            for c in get_children(length, v[0]):
                if c not in v[2]:
                    temp_set = v[2].copy()
                    temp_set.add(c)
                    temp = (c, v[1] + 1, temp_set)
                    fringe.append(temp)
    return None

def id_dfs(string):
    max_depth = 0
    result = None
    goal = ''.join(sorted(string))[1:] + '.'
    length = int(len(string)**(1/2))
    while result is None:
        result = kdfs(string, max_depth, goal, length)
        max_depth += 1
    return result


with open(sys.argv[1], "r") as f:
    line_list = [line.strip() for line in f]

    for i, puzzle in enumerate(line_list):
        # bfs time
        bfs_start_time = perf_counter()
        bfs_result = bfs(puzzle, ''.join(sorted(puzzle))[1:] + '.')
        bfs_end_time = perf_counter()

        # dfs time
        id_dfs_start_time = perf_counter()
        id_dfs_result = id_dfs(puzzle)
        id_dfs_end_time = perf_counter()

        if bfs_result is not None:
            print("Line " + str(i) + ": " + puzzle + ", BFS - " + str(bfs_result) + " moves in " + str(bfs_end_time - bfs_start_time) + " seconds")
        else:
            print("Line " + str(i) + ": " + puzzle + ", no solution determined for BFS")

        if id_dfs_result is not None:
            print("Line " + str(i) + ": " + puzzle + ", ID-DFS - " + str(id_dfs_result) + " moves in " + str(id_dfs_end_time - id_dfs_start_time) + " seconds")
        else:
            print("Line " + str(i) + ": " + puzzle + ", no solution determined for ID-DFS")
        print()

#!/usr/bin/env python3

import sys

puzzles = []
with open(sys.argv[1]) as file:
    for line in file:
        size, board = line.strip().split()
        size = int(size)
        puzzle = []
        for i in range(0, size*size, size):
            puzzle.append(list(board[i:i+size]))
        puzzles.append(puzzle)

def print_puzzle(size, board):
    flat_board = [char for row in board for char in row]
    rows = [' '.join(flat_board[i:i+size]) for i in range(0, size*size, size)]
    print('\n'.join(rows))


def find_goal(board):
    flat_board = ''.join([''.join(row) for row in board])
    return "".join(sorted(flat_board.replace(".", ""))) + "."

def get_children(state):
    children = []
    size = len(state)
    for i in range(size):
        for j in range(size):
            if state[i][j] == '.':
                if i > 0:
                    child = [row[:] for row in state]
                    child[i][j], child[i-1][j] = child[i-1][j], child[i][j]
                    children.append(child)
                if i < size-1:
                    child = [row[:] for row in state]
                    child[i][j], child[i+1][j] = child[i+1][j], child[i][j]
                    children.append(child)
                if j > 0:
                    child = [row[:] for row in state]
                    child[i][j], child[i][j-1] = child[i][j-1], child[i][j]
                    children.append(child)
                if j < size-1:
                    child = [row[:] for row in state]
                    child[i][j], child[i][j+1] = child[i][j+1], child[i][j]
                    children.append(child)
    return children
            
for i, puzzle in enumerate(puzzles):
    print(f"Line ", i, " start state:")
    print_puzzle(len(puzzle),puzzle)
    goal_state = find_goal(puzzle)
    print(f"Line ", i , " goal state: ", goal_state)
    children = get_children(puzzle)
    child_strings = ["".join(["".join(row) for row in child]) for child in children]
    print("Line ", i, " children: ", child_strings, "\n")

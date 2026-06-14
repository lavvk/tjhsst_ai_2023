import math
import sys
def read_puzzles(filename):
    with open(filename) as f:
        return [line.strip() for line in f]


def set_up_variables(cur_line):
    global N, subblock_height, subblock_width, symbol_set
    N = int(math.sqrt(len(cur_line)))

    if int(math.sqrt(N)) ** 2 == N:
        subblock_height = subblock_width = int(math.sqrt(N))
    else:
        subblock_height, subblock_width = find_subblock_dimensions(N)

    symbol_set = set("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:N])

def find_subblock_dimensions(N):
    for i in range(int(math.sqrt(N)), 0, -1):
        if N % i == 0:
            subblock_height = i
            break
    for i in range(int(math.sqrt(N)) + 1, N):
        if N % i == 0:
            subblock_width = i
            break
    return subblock_height, subblock_width

def print_board(line_str):
    board = ""
    for i in range(subblock_height):
        for j in range(subblock_width):
            start_index = (i * subblock_height * N) + (j * subblock_width)
            end_index = start_index + subblock_width
            board += line_str[start_index:end_index] + ' | '
        board = board[:-2]  # remove the last separator and add a newline
        board += '\n'

        if (i + 1) % subblock_height == 0 and i + 1 != subblock_height:
            board += '- ' * (N + subblock_width - 1) + '\n'

    return board


def set_up_constraints(cur_line):
    global rows, cols, blocks
    rows = [set() for _ in range(N)]
    cols = [set() for _ in range(N)]
    blocks = [[set() for _ in range(N // subblock_width)] for _ in range(N // subblock_height)]

    for i in range(N ** 2):
        if cur_line[i] == '.':
            continue
        block_constraint, row_constraint, col_constraint = get_constraints(i)
        block_constraint.add(cur_line[i])
        row_constraint.add(cur_line[i])
        col_constraint.add(cur_line[i])

def get_constraints(i):
    row_i = i // N
    col_i = i % N
    block_constraint = blocks[row_i // subblock_height][col_i // subblock_width]
    row_constraint = rows[row_i]
    col_constraint = cols[col_i]
    return block_constraint, row_constraint, col_constraint

def symbol_counts(line_str):
    return {c: line_str.count(c) for c in symbol_set}

def csp_backtracking(state):
    if goal_test(state):
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = state[:var] + val + state[var + 1:]
        block_constraint, row_constraint, col_constraint = get_constraints(var)
        block_constraint.add(val)
        row_constraint.add(val)
        col_constraint.add(val)
        result = csp_backtracking(new_state)
        if result is not None:
            return result
        else:
            block_constraint.remove(val)
            row_constraint.remove(val)
            col_constraint.remove(val)
    return None

def goal_test(state):
    return '.' not in state

def get_next_unassigned_var(state):
    return state.index('.')

def get_sorted_values(state, var):
    block_constraint, row_constraint, col_constraint = get_constraints(var)
    return sorted(set.intersection(symbol_set - block_constraint, symbol_set - row_constraint, symbol_set - col_constraint))

puzzles = read_puzzles("puzzles_1_standard_easy.txt")

for cur_line in puzzles:
    set_up_variables(cur_line)
    set_up_constraints(cur_line)

    solution = csp_backtracking(cur_line)
    print(solution)

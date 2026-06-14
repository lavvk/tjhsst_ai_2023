import numpy as np
import sys
import ast


def initialize_q_values(n, goal_squares):
    q_values = np.full((n, n, 2**(len(magic_items))), -np.inf)
    for goal in goal_squares:
        row, col = divmod(goal, n)
        q_values[row, col, 0] = -1000000  
    return q_values

def get_possible_moves(state, n):
    row, col, magic_items_state = state
    moves = []
    if row > 0:
        moves.append((row-1, col, magic_items_state))  # up
    if row < n-1:
        moves.append((row+1, col, magic_items_state))  # down
    if col > 0:
        moves.append((row, col-1, magic_items_state))  # left
    if col < n-1:
        moves.append((row, col+1, magic_items_state))  # right
    return moves

def update_q_values(q_values, n, goal_squares, quicksand_pits, magic_items, num_items_needed, warps):
    quicksand_indices = {q: divmod(q, n) for q in quicksand_pits}
    magic_item_indices = {q: divmod(q, n) for q in magic_items}
    warp_indices = {w[0]: (divmod(w[0], n), divmod(w[1], n), w[2]) for w in warps}

    while True:
        new_q_values = np.copy(q_values)
        for row in range(n):
            for col in range(n):
                for magic_items_state in range(2**(len(magic_items))):
                    if (row * n + col) in goal_squares:
                        if sum(1 for i in range(len(magic_items)) if (magic_items_state >> i) & 1) >= num_items_needed:
                            reward = -99 if (row, col) in quicksand_indices.values() else 0
                        else:
                            reward = -1000000
                        new_q_values[row, col, magic_items_state] = reward
                        continue

                    possible_moves = get_possible_moves((row, col, magic_items_state), n)
                    max_q = -np.inf

                    for move in possible_moves:
                        move_row, move_col, move_magic_items_state = move
                        move_loc = move_row * n + move_col
                        reward = -1

                        if (row, col) in quicksand_indices.values():
                            reward = -100

                        if (row, col) in magic_item_indices.values():
                            move_magic_items_state = magic_items_state | (1 << list(magic_item_indices.values()).index((row, col)))

                        if move_loc in warp_indices:
                            (orig_row, orig_col), (warp_row, warp_col), prob = warp_indices[move_loc]
                            max_q = max(max_q, (1 - prob) * q_values[move_row, move_col, move_magic_items_state] + 
                                            prob * q_values[warp_row, warp_col, move_magic_items_state] + reward)
                        else:
                            max_q = max(max_q, q_values[move_row, move_col, move_magic_items_state] + reward)
                    
                    new_q_values[row, col, magic_items_state] = max_q

        if np.array_equal(new_q_values, q_values):
            break
        q_values = new_q_values

    return q_values

def format_output(q_values, goal_squares, n):
    output = ""
    for row in range(n):
        row_output = []
        for col in range(n):
            if (row * n + col) in goal_squares:
                row_output.append("x")
            else:
                row_output.append("%.2f" % q_values[row, col, 0])
        output += "\t".join(row_output) + "\n"
    return output.strip()

# sample cases
# cases = [
#     {
#         "size": 5,
#         "goals": [0],
#         "fire_squares": [],
#         "necessary_items": 0,
#         "magic_items": [],
#         "warps": [(19, 1, 0.9)]
#     },
#     {
#         "size": 5,
#         "goals": [0],
#         "fire_squares": [],
#         "necessary_items": 0,
#         "magic_items": [],
#         "warps": [(19, 1, 0.5)]
#     },
#     {
#         "size": 5,
#         "goals": [0],
#         "fire_squares": [],
#         "necessary_items": 0,
#         "magic_items": [],
#         "warps": [(19, 1, 0.1)]
#     },
#     {
#         "size": 5,
#         "goals": [0],
#         "fire_squares": [23, 18, 13, 14],
#         "necessary_items": 0,
#         "magic_items": [],
#         "warps": [(19, 1, 0.1)]
#     },
#     {
#         "size": 5,
#         "goals": [0],
#         "fire_squares": [23, 18, 19],
#         "necessary_items": 0,
#         "magic_items": [],
#         "warps": [(19, 1, 0.1)]
#     },
#     {
#         "size": 5,
#         "goals": [0],
#         "fire_squares": [1, 6, 11, 16, 23, 18, 13, 8],
#         "necessary_items": 0,
#         "magic_items": [],
#         "warps": [(5, 24, 0.1)]
#     },
#     {
#         "size": 5,
#         "goals": [0],
#         "fire_squares": [19],
#         "necessary_items": 1,
#         "magic_items": [19],
#         "warps": [(19, 1, 0.1)]
#     },
#     {
#         "size": 5,
#         "goals": [0, 21],
#         "fire_squares": [16, 5, 4],
#         "necessary_items": 2,
#         "magic_items": [10, 18, 19],
#         "warps": [(19, 1, 0.1), (2, 5, 0.2), (7, 6, 0.3), (20, 4, 0.7)]
#     },
#     {
#         "size": 5,
#         "goals": [0, 21],
#         "fire_squares": [16, 9, 12],
#         "necessary_items": 2,
#         "magic_items": [9, 3, 18],
#         "warps": [(19, 1, 0.1), (2, 5, 0.2), (7, 6, 0.3), (20, 4, 0.7)]
#     }
# ]

# # Process each case
# for case in cases:
#     n = case["size"]
#     goal_squares = case["goals"]
#     quicksand_pits = case["fire_squares"]
#     num_items_needed = case["necessary_items"]
#     magic_items = case["magic_items"]
#     warps = case["warps"]

#     print(f"size: {n}")
#     print(f"goals: {goal_squares}")
#     print(f"fire squares: {quicksand_pits}")
#     print(f"necessary items: {num_items_needed}")
#     print(f"magic items: {magic_items}")
#     print(f"warps: {warps}")

#     q_values = initialize_q_values(n, goal_squares)
#     q_values = update_q_values(q_values, n, goal_squares, quicksand_pits, magic_items, num_items_needed, warps)
#     output = format_output(q_values, goal_squares, n)
#     print(output)
#     print()

n = int(sys.argv[1])
goal_squares = ast.literal_eval(sys.argv[2])
quicksand_pits = ast.literal_eval(sys.argv[3])
num_items_needed = int(sys.argv[4])
magic_items = ast.literal_eval(sys.argv[5])
warps = ast.literal_eval(sys.argv[6])


q_values = initialize_q_values(n, goal_squares)
q_values = update_q_values(q_values, n, goal_squares, quicksand_pits, magic_items, num_items_needed, warps)
output = format_output(q_values, goal_squares, n)
print(output)
print()
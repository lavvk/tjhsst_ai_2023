import time

def goal_test(state):
    return None not in state

def get_next_unassigned_var(state):
    return state.index(None)

def get_sorted_values(state, row):
    curr = []  
    for i in range(len(state)):
        if state[i] is not None:
            curr.append(state[i])
    
    valid_indices = []
    for j in range(len(state)):
        if j not in curr:
            is_good = True
            for i in range(len(state)):
                if state[i] is not None and i != row and (state[i] == j or abs(state[i] - j) == abs(i - row)):
                    is_good = False
                    break
            if is_good:
                valid_indices.append(j)
    
    sorted_possibles = sorted(valid_indices, key=lambda x: abs(x - len(state) / 2))
    
    return sorted_possibles

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

def csp_backtracking(state):
    if goal_test(state):
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = state[:var] + [val] + state[var+1:]
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

board_size = 31  
board = []  
for i in range(board_size):
    board.append(None)
    
    
time1 = time.perf_counter()
final_board = csp_backtracking(board)

print(final_board)
print(test_solution(final_board))

board_size = 33  
board = []  
for i in range(board_size):
    board.append(None)
    
    
# time1 = time.perf_counter()
final_board = csp_backtracking(board)
time2 = time.perf_counter()

print(final_board)
print(test_solution(final_board))
print(time2 - time1, "seconds")



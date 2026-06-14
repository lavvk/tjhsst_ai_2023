
import time
from random import randint

def generate_state(length):
    state = []
    for i in range(length):
        state.append(randint(0, length - 1))
    return state

def get_conflicts(state):
    conflicts = [0] * len(state)
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts[i] += 1
                conflicts[j] += 1
    return conflicts


def goal_test(state):
    conflicts = get_conflicts(state)
    if sum(conflicts) == 0:
        return False
    else:
        return conflicts

def get_next_unassigned_var(state):
    return state.index(None)

def get_idxes(conflicts):
    max_conflict = max(conflicts)
    ways = [(conflict, i) for i, conflict in enumerate(conflicts) if conflict == max_conflict]
    return ways

def get_sorted_values(state, row):
    ways = [
        (sum(get_conflicts(state[:row] + [idx] + state[row + 1:])), state[:row] + [idx] + state[row + 1:])
        for idx in range(len(state))
    ]
    min_moves = min(ways, key=lambda x: x[0])[0]
    fin_ways = [temp for conflict, temp in ways if conflict == min_moves]
    return fin_ways


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

def incremental(state, path):
    conflicts = goal_test(state)
    if conflicts == False:
        return state, path + str(state) + ", Conflicts: 0"
    path += str(state) + ", Conflicts: " + str(sum(conflicts)) + "\n"
    idxes = get_idxes(conflicts)
    rand = randint(0, len(idxes) - 1)
    ways = get_sorted_values(state, idxes[rand][1])
    rand = randint(0, len(ways) - 1)
    result = incremental(ways[rand], path)
    if result is not None:
        return result
    return None

board_size = 33
board_1 = generate_state(board_size)
time1 = time.perf_counter()
result = incremental(board_1, "")
print(result[1])
print(test_solution(result[0]))
time1 = time.perf_counter()
time2 = time.perf_counter()

print(time2 - time1, "secs")


board_size = 35
board_1 = generate_state(board_size)
time1 = time.perf_counter()
result = incremental(board_1, "")
print(result[1])
print(test_solution(result[0]))
time1 = time.perf_counter()
time2 = time.perf_counter()

print(time2 - time1, "secs")
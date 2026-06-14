import math
import sys

symbol_set = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def print_puzzle(values, string):
    row_length, row_skip, word_skip = values

    for i in range(0, len(string), row_length):
        row = ' '.join(' '.join(string[j:j + word_skip]) for j in range(i, i + row_length, word_skip)) + ' '
        print(row.strip())

        if (i // row_length) % row_skip == row_skip - 1:
            print()

    return ''

def vals(string):
    n = int(math.sqrt(len(string)))
    sq = int(math.sqrt(n))
    if sq ** 2 != n:
        while n % sq != 0:
            sq -= 1
    height = sq
    width = n // height
    symbols = symbol_set[:n]
    sub_blocks = len(string) // (width * height)
    return n, height, width, sub_blocks, symbols

def get_neighbors(values, string):
    neighbors = {'row': {i: [] for i in range(values[0])}, 'col': {i: [] for i in range(values[0])},
                 'sub-block': {i: [] for i in range(values[3])}}
    constraint = {i: [] for i in range(len(string))}
    for i in range(len(string)):
        r = (i // values[0])
        c = (i % values[0])
        sb = values[1] * (r // values[1]) + (c // values[2])
        neighbors['row'][r] += [i]
        neighbors['col'][c] += [i]
        neighbors['sub-block'][sb] += [i]
        constraint[i] = [r, c, sb]
    return neighbors, constraint

def goal_test(neighbors, values, string):
    check = {char: string.count(char) for char in values[-1]}
    for key in check:
        if check[key] != values[0]:
            return False
    return True

def positions(neighbors, constraint, values, string):
    positions_dict = {
        i: positions_helper(neighbors, constraint, values, string, i)  
        for i in range(len(string))  
        if string[i] == '.' 
    }
    return positions_dict

def positions_helper(neighbors, constraint, values, string, index):
    if string[index] != '.':
        return []

    pos = values[-1]
    constraint_vals = constraint[index]
    used = set()

    for i in neighbors['row'][constraint_vals[0]]:
        used.add(string[i])

    for i in neighbors['col'][constraint_vals[1]]:
        used.add(string[i])

    for i in neighbors['sub-block'][constraint_vals[2]]:
        used.add(string[i])

    return [val for val in pos if val not in used]

def get_next_unassigned_var(string):
    for i in range(len(string)):
        if string[i] == '.':
            return i
    return None

def csp_backtracking(neighbors, constraint, values, string):
    if goal_test(neighbors, values, string):
        return string
    var = get_next_unassigned_var(string)
    for val in positions_helper(neighbors, constraint, values, string, var):
        new_state = string[:var] + val + string[var + 1:]
        result = csp_backtracking(neighbors, constraint, values, new_state)
        if result is not None:
            return result
    return None

def forward_looking(d, neighbors, constraint, values, string):
    s = string
    if goal_test(neighbors, values, s):
        return True, s
    for i in d.keys():
        if len(d[i]) == 1:
            s = s[:i] + d[i][0] + s[i + 1:]
            grps = constraint[i]
            vals = [j for j in neighbors['row'][grps[0]] if j != i and j in d.keys()] + [
                j for j in neighbors['col'][grps[1]] if j != i and j in d.keys()] + [
                       j for j in neighbors['sub-block'][grps[2]] if j != i and j in d.keys()]
            for j in vals:
                if d[i][0] in d[j]:
                    if len(d[j]) == 1:
                        return False, None
                    d[j].remove(d[i][0])
    if s == string:
        return False, string
    return forward_looking(d, neighbors, constraint, values, s)

def backtracking(d, neighbors, constraint, values, string):
    if goal_test(neighbors, values, string):
        return string
    var = None
    vals = [len(d[key]) for key in d.keys() if len(d[key]) != 1]
    if len(vals) > 0:
        minVals = min(vals)
        for key in d.keys():
            if len(d[key]) == minVals:
                var = key
                break
    if var is not None:
        for val in d[var]:
            new_state = string[:var] + val + string[var + 1:]
            new_d = positions(neighbors, constraint, values, new_state)
            _, board = forward_looking(new_d, neighbors, constraint, values, new_state)
            if board is not None:
                _, diff = constraint_propagation_all(new_d, neighbors, constraint, values, board)
                if diff is not None:
                    result = backtracking(new_d, neighbors, constraint, values, diff)
                    if result is not None:
                        return result
    return None

def constraint_propagation_all(d, neighbors, constraint, values, string):
    s = string
    if goal_test(neighbors, values, s):
        return True, s
    for pos in [neighbors['sub-block'], neighbors['row'], neighbors['col']]:
        for i in pos.keys():
            grp = [s[j] for j in pos[i]]
            for ch in values[-1]:
                if ch not in grp:
                    idx = -1
                    for val in pos[i]:
                        if val in d.keys():
                            if ch in d[val]:
                                if len(d[val]) == 1:
                                    idx = val
                                else:
                                    if idx == -1:
                                        idx = val
                                    else:
                                        idx = -2
                    if idx != -1 and idx != -2:
                        s = s[:idx] + ch + s[idx + 1:]
                        d.pop(idx)
                        _, board = forward_looking(d, neighbors, constraint, values, s)
                        if board is not None:
                            _, diff = constraint_propagation_all(d, neighbors, constraint, values, board)
                            if diff is not None:
                                return True, diff
                            else:
                                return False, None
                    elif idx == -2:
                        continue
                    else:
                        return False, None
    if s == string:
        return False, s
    return forward_looking(d, neighbors, constraint, values, s)

with open(sys.argv[1], "r") as f:
    lines = []
    line_list = [line.strip() for line in f]
    for i in range(len(line_list)):
        value = vals(line_list[i])
        neighbors, constraint = get_neighbors(value, line_list[i])
        pos = positions(neighbors, constraint, value, line_list[i])
        is_solved, p = forward_looking(pos, neighbors, constraint, value, line_list[i])
        if is_solved:
            lines.append(p)
        else:
            lines.append(backtracking(positions(neighbors, constraint, value, p), neighbors, constraint, value, p))
    for i, line in enumerate(lines):
        print(line)

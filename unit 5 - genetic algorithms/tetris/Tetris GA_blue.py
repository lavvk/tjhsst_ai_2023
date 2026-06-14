import sys

initial_board = sys.argv[1]
# initial_board = ("          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########")
board = [list(initial_board[i:i + 10]) for i in range(0, len(initial_board), 10)]  ## 2d arr
max = {i: 0 for i in range(10)}

i_info = { 0: (1, 4, [0, 0, 0, 0], [1, 1, 1, 1]), 1: (4, 1, [0], [4]) }

o_info = { 0: (2, 2, [0, 0], [2, 2]) }

t_info = { 0: (2, 3, [0, 0, 0], [1, 2, 1]), 1: (3, 2, [0, -1], [3, 1]), 2: (2, 3, [0, 1, 0], [1, 2, 1]), 3: (3, 2, [0, 1], [1, 3]) }

s_info = { 0: (2, 3, [0, 0, -1], [1, 2, 1]), 1: (3, 2, [0, 1], [2, 2]) }

z_info = { 0: (2, 3, [0, 1, 1], [1, 2, 1]), 1: (3, 2, [0, -1], [2, 2]) }

j_info = { 0: (2, 3, [0, 0, 0], [2, 1, 1]), 1: (3, 2, [0, -2], [3, 1]), 2: (2, 3, [0, 0, 1], [1, 1, 2]), 3: (3, 2, [0, 0], [1, 3]) }

l_info = { 0: (2, 3, [0, 0, 0], [1, 1, 2]), 1: (3, 2, [0, 0], [3, 1]), 2: (2, 3, [0, -1, -1], [2, 1, 1]), 3: (3, 2, [0, 2], [1, 3]) }

everything = {'I': i_info, 'O': o_info, 'T': t_info, 'S': s_info, 'Z': z_info, 'J': j_info, 'L': l_info }


def get_col_disp(idx, info, max):
    col_disp = []
    for c in range(idx, idx + info[1]):
        col_disp.append((c, max[idx] - max[c]))
    return col_disp


def place_piece(board, info, idx, max):
    if idx + info[1] > 10:
        return None, None

    col_disp = get_col_disp(idx, info, max)
    cols_loco = [col for col, _ in col_disp]

    disp = []
    for count, (col, val) in enumerate(col_disp):
        disp.append((col, val - info[2][count], count))

    col_loco, v, count_in_list = min(disp, key=lambda t: t[1])

    initial_loco = 20 - max[col_loco] - 1

    new_disp = [info[2][i] - info[2][count_in_list] for i in range(info[1])]

    for count, col in enumerate(cols_loco):
        loco = initial_loco + new_disp[count]
        curr = info[3][count]
        while curr > 0:
            if loco < 0:
                return None, None
            board[loco][col] = '#'
            loco -= 1
            curr -= 1

    num = 0
    new = [row[:] for row in board]
    
    for row in range(len(board)):
        cleared = True
        for cell in board[row]:
            if cell != '#':
                cleared = False
                break
        if cleared:
            new.pop(row)
            new.insert(0, [' '] * 10)
            num += 1

    total = {1: 40, 2: 100, 3: 300, 4: 1200}.get(num, 0)

    return new, total

fin_boards = []
for type, oris in everything.items():
    for ori, d in oris.items():
        for idx in range(0, 10 - d[1] + 1):
            new = [row[:] for row in board]
            new_max = {}
            for col in range(10):
                for row in range(20):
                    if new[row][col] != ' ':
                        new_max[col] = 20 - row
                        break
                else:
                    new_max[col] = 0
            temp_max = new_max
            new, pts = place_piece(new, d, idx, temp_max)
            fin_boards.append(new)


def format(board):
    fin_string = ''
    for mini in board:
        for c in mini:
            fin_string += c
    return fin_string


with open('tetrisout.txt', 'w') as f:
    for board in fin_boards:
        if board is None:
            f.write('GAME OVER\n')
        else:
            f.write(format(board) + '\n')

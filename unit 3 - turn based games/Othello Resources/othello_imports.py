
def possible_moves(board, token):
    dir = [-11, -10, -9, -1, 1, 9, 10, 11]
    indexes = []
    opp = "o" if token == "x" else "x"
    
    for ind, item in enumerate(board):
        if item == ".":
            for n in dir:
                curr = ind + n
                if board[curr] == opp:
                    temp_indexes = []
                    while board[curr] == opp:
                        temp_indexes.append(curr)
                        curr += n
                    if board[curr] == token:
                        indexes.append(ind)
                        break
    
    return indexes


def make_move(board, token, index):
    dir = [-11, -10, -9, -1, 1, 9, 10, 11]
    if (token == 'x'):
        opponent = 'o'
    else:
        opponent = 'x'
    moves = []
    
    for path in dir:
        val = index + path
        if board[val] == opponent:
            increment = path
            flip_indexes = []
            while board[val] == opponent:
                flip_indexes.append(val)
                val += increment
            if board[val] == token:
                moves.extend(flip_indexes)
                
    new_board = list(board)
    new_board[index] = token
    
    for i in moves:
        new_board[i] = token
    
    return ''.join(new_board)

import sys

## red testing
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


def early_game(board):
    if board.count(".")>= 48:
        return True
    
def score(board):
    score = 0
    if len(possible_moves(board, "x")) == 0 and len(possible_moves(board, "o")) == 0:
        if board.count("x") > board.count("o"):
            score = 10000 
        elif board.count("o") > board.count("x"):
            score = -10000 
        return score
    corners_dict = {11: {12,21,22}, 18:{17,27,28}, 88: {87,77,78}, 81:{71,71,82}}
    for corner, adjacents in corners_dict.items():
        if board[corner] == "x":
            score += 5000
            for adjacent in adjacents:
                if board[adjacent] == "x":
                    score += 100
        elif board[corner] == "o":
            score -= 5000
            for adjacent in adjacents:
                if board[adjacent] == "o":
                    score -= 100
        else:
            for adjacent in adjacents:
                if board[adjacent] == "x":
                    score -= 1000
                elif board[adjacent] == "o":
                    score += 1000
    borders = [board[13], board[14], board[15], board[16], board[31], board[41], board[51], board[61], board[83], board[84], board[85], board[86], board[68], board[58], board[48], board[38]]
    for border in borders:
        if border == "x":
            score += 2500
        elif border == "o":
            score -=2500
    penalty = 0
    if early_game(board):
        penalty = 5000*(board.count('x')-board.count('o'))
    score +=  len(possible_moves(board, "x")) * 5000000
    score -= len(possible_moves(board, "o")) * 150
    score -= penalty
    return score

def max_step(board, depth, alpha, beta):
    if len(possible_moves(board, "x")) == 0 and len(possible_moves(board, "o")) == 0 or depth == 0:
        return score(board)
    if len(possible_moves(board, "x")) == 0:
        return min_step(board, depth - 1, alpha, beta)
    results = []
    for index in possible_moves(board, "x"):
        next_board = make_move(board, "x", index)
        results.append(min_step(next_board, depth - 1, alpha, beta))
        added = results[-1]
        
        # ALPHA/BETA PRUNING HERE
        if alpha <= added:
            alpha = added
        if beta <= alpha:
            break
    return max(results)

def min_step(board, depth, alpha, beta):
    if  len(possible_moves(board, "x")) == 0 and len(possible_moves(board, "o")) == 0 or depth == 0:
        return score(board)
    if len(possible_moves(board, "o")) == 0:
        return max_step(board, depth - 1, alpha, beta)
    results = []
    for index in possible_moves(board, "o"):
        next_board = make_move(board, "o", index)
        results.append(max_step(next_board, depth - 1, alpha, beta))
        added = results[-1]
        # ALPHA/BETA PRUNING HERE
        if beta >= added:
            beta = added
        if beta <= alpha:
            break
    return min(results)


def find_next_move(board, player, depth): ## split up x and o bc i was struggling last time 
    results = []
    copy = board
    if player == "x":
            for index in possible_moves(board, "x"):
                next_board = make_move(copy, "x", index)
                results.append((min_step(next_board, depth, -100000000000000, 100000000000000), index))
            mx,ind = max(results)
            return ind
    else:
        for index in possible_moves(board, "o"):
            next_board = make_move(copy, "o", index)
            results.append((max_step(next_board, depth, -1000000000000000, 1000000000000000), index))
        mn,ind = min(results)
        return ind




## test file

board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1
## server

# class Strategy():
#    logging = True  # Optional
#    uses_10x10_board = True  # If you delete this line, the server will give you a 64-character 8x8 board instead
#    uses_10x10_moves = True  # If you delete this line, the server will expect indices on an 8x8 board instead
#    def best_strategy(self, board, player, best_move, still_running):
#        depth = 1
#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
#            best_move.value = find_next_move(board, player, depth) 
#            depth += 1
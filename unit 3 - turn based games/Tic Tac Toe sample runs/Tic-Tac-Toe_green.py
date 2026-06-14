import sys

nums = "012345678"

def assign_x_o():
    puzzle = sys.argv[1]
    comp_turn = True
    computer = ''
    player = ''

    if puzzle.count('.') == 9:
        val = input("Should I be X or O? ")
        if val != 'X':
            comp_turn = False
        else:
            comp_turn = True

        if val == 'X':
            computer = 'X'
            player = 'O'
        else:
            computer = 'O'
            player = 'X'

    else:
        if puzzle.count('X') == puzzle.count('O'):
            computer = 'X'
            player = 'O'
        else:
            computer = 'O'
            player = 'X'
            
    return puzzle, comp_turn, computer, player

def display_board(board):
    print("\nCurrent board: ")
    
    for i in range(0, len(board), 3):
        current_row = "".join(board[i:i + 3])
        nums_row = nums[i:i + 3]
        print(current_row + "\t" + nums_row)
    
    print()

def game_result(score):
    if score == 0:
        return "We tied!"
    elif score == 1:
        return "I win!" if computer == "X" else "You win!"
    else:
        return "I win!" if computer == "O" else "You win!"

def end(board):
    x = set()
    o = set()

    for i, val in enumerate(board):
        if val == "X":
            x.add(i)
        elif val == "O":
            o.add(i)

    win_states = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

    for state in win_states:
        if state.issubset(x):
            return 1
        elif state.issubset(o):
            return -1

    if board.count(".") == 0:
        return 0

    return -2

def max_step(board, comp_turn):
    score = end(board)
    if score != -2:
        return score
    current_player = computer if comp_turn else player
    results = []
    for place in range(len(board)):
        if board[place] == ".":
            updated = board[:place] + (computer if comp_turn else player) + board[place + 1:]
            results.append(min_step(updated, not comp_turn))

    return max(results) if current_player == "X" else min(results)

def min_step(board, comp_turn):
    score = end(board)
    if score != -2:
        return score
    current_player = computer if comp_turn else player
    results = []
    for place in range(len(board)):
        if board[place] == ".":
            updated = board[:place] + (computer if comp_turn else player) + board[place + 1:]
            results.append(max_step(updated, not comp_turn))

    return max(results) if current_player == "X" else min(results)

def print_moves_neater(moves, positions, computer):
    if computer == 'X':
        loss = -1
    else:
        loss = 1
    if computer == 'X':
        win = 1
    else:
        win = -1
    for i, move in enumerate(moves):
        if move == win:
            print("Moving at", nums[positions[i]], "results in a win.")
        elif move == loss:
            print("Moving at", nums[positions[i]], "results in a loss.")
        else:
            print("Moving at", nums[positions[i]], "results in a tie.")

def choose(moves, ind):
    best_move = max(moves) if computer == "X" else min(moves)
    return ind[moves.index(best_move)]

def game(board, comp_turn):
    display_board(board)
    score = end(board)
    
    if score != -2:
        return game_result(score)

    positions = [ch for ch in range(len(board)) if board[ch] == "."]

    if comp_turn:
        moves = []
        for i, index in enumerate(positions):
            updated = board[:index] + computer + board[index + 1:]
            move_score = min_step(updated, not comp_turn)
            moves.append(move_score)

        print_moves_neater(moves, positions, computer)

        index = choose(moves, positions)
        print("\nI chose space " + nums[index] + ".")
        board = board[:index] + computer + board[index + 1:]
        return game(board, not comp_turn)
    else:
        pos_str = ", ".join([str(pos) for pos in positions]) + "."
        print("You can move to any of these spaces: " + pos_str)
        index = int(input("Your choice? "))
        board = board[:index] + player + board[index + 1:]
        return game(board, not comp_turn)

board, comp_turn, computer, player = assign_x_o()
print(game(board, comp_turn))

from othello_imports import possible_moves, make_move
from random import choice
import sys

corners_dict = {
    11: {12, 21, 22},
    18: {17, 27, 28},
    81: {71, 72, 82},
    88: {87, 78, 77}
}

board = sys.argv[1]
player = sys.argv[2]
possibles = possible_moves(board, player)
discarded = []
corners = []
other = []
for move in possibles:
    used = False
    for corner, adjacents in corners_dict.items():
        if move in adjacents and board[corner] != player:
            discarded.append(move)
            used = True
    if move in corners_dict:
        corners.append(move)
        used = True
    if not used:
        other.append(move)
if len(corners) > 0:
    print("corner!")
    print(choice(corners))
elif len(other) + len(corners) == 0:
    print("no options!")
    print(choice(discarded))
else:
    possibilities = []
    for move in other:
        new_board = make_move(board, player, move)
        possibilities.append((new_board.count(player), move))
    possibilities.sort()
    if len(possibilities) > 1:
        decision = choice([-1, -2])
    else:
        decision = -1
    print(possibilities[decision][1])
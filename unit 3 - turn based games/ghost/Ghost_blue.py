import sys

min_len = int(sys.argv[2])

continues = "" if len(sys.argv) < 4 else sys.argv[3]

lines = []
alph = "abcdefghijklmnopqrstuvwxyz"

with open(sys.argv[1]) as f:
    for l in f:
        l = l.strip().lower()
        if all(c in alph for c in l):
            if l.startswith(continues) and len(l) >= min_len:
                lines.append(l)

def poss_letter(w, poss_words):
    letter = {}
    w_len = len(w)

    for poss_w in poss_words:
        if len(poss_w) > w_len:
            curr_letter = poss_w[w_len]
            if curr_letter not in letter:
                letter[curr_letter] = []
            letter[curr_letter].append(poss_w)

    return letter

def min_step(w, poss_words):
    if w in poss_words:
        return -1

    children = []
    poss_moves = poss_letter(w, poss_words)

    for child in poss_moves.keys():
        new_w = w + child
        result = max_step(new_w, poss_moves[child])
        children.append(result)

    return min(children)

def max_step(w, poss_words):
    if w in poss_words:
        return 1

    children = []
    poss_moves = poss_letter(w, poss_words)

    for child in poss_moves.keys():
        new_w = w + child
        result = min_step(new_w, poss_moves[child])
        children.append(result)

    return max(children)

win_let = []
moves = poss_letter(continues, lines)

for char in moves.keys():
    new_w = continues + char
    result = min_step(new_w, moves[char])
    if result == 1:
        win_let.append(char)

if win_let:
    print("Next player can guarantee victory by playing any of these letters: " + str(win_let))
else:
    print("Next player will lose!")

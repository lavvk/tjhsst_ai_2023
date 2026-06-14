import random

POPULATION_SIZE = 100  # score w popsize 50 fluctuated too much after each gen
NUM_CLONES = 25
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = 0.75
MUTATION_RATE = 0.01

pieces = {
    'I': {1: ['****'], 4: ['****']},
    'O': {2: ['****']},
    'T': {2: ['* *** ', ' *** *'], 3: [' * ***', '*** * ']},
    'S': {2: ['* ** *'], 3: [' **** ']},
    'Z': {2: [' **** '], 3: ['**  **']},
    'J': {2: ['*** * ', ' * ***'], 3: ['*  ***', '***  *']},
    'L': {2: ['* * **', '** * *'], 3: ['  ****', '****  ']}
}

differences = {}
for piece_type, orientations in pieces.items():
    differences[piece_type] = {}
    for size, piece_list in orientations.items():
        differences[piece_type][size] = []
        for piece in piece_list:
            net = []
            n = size * ((len(piece) // size) - 1)
            for i in range(size):
                for j in range(i + n, i, -size):
                    if piece[j] == '*':
                        break
                    if piece[j] == ' ' and piece[j - size] != ' ':
                        net += [-(i + n + size - j) // size]
                        break
                if len(net) != i + 1:
                    net += [0]
            differences[piece_type][size].append(net)

def place_piece(state, place, piece, difference, columns):
    n = len(piece) // len(difference)
    c = [columns[i + place] - difference[i] - n for i in range(len(difference))]
    ind = min(c)
    if ind < 0:
        return 'GAME OVER'
    temp = list(state)
    for i, v in enumerate(piece):
        if v == '*':
            temp[(ind + (i // len(difference))) * 10 + place + (i % len(difference))] = '#'
    state = ''.join(temp)
    return state


def play_game(strategy, graphics):
    board = ''.join([' ' for _ in range(200)])
    points = 0
    while board != 'GAME OVER':
        can_move = False
        best = ('', -999999999)
        piece_type = random.choice(list(pieces.keys()))
        columns = []
        for i in range(10):
            for j in range(i, 200, 10):
                if board[j] == '#':
                    columns.append((j - i) // 10)
                    break
            if len(columns) != i + 1:
                columns.append(20)
        for size in pieces[piece_type].keys():
            for ind, piece in enumerate(pieces[piece_type][size]):
                for i in range(0, 10 - size + 1):
                    pos_board = place_piece(board, i, piece, differences[piece_type][size][ind], columns)
                    if pos_board == 'GAME OVER':
                        break
                    can_move = True
                    
                    a, b, c, d = strategy
                    rows = [pos_board[i:i + 10].count('#') for i in range(0, 200, 10)]
                    cols = [[pos_board[j] for j in range(i, 200, 10)] for i in range(10)]
                    tops = []
                    for i in range(10):
                        tops.append(20 - cols[i].index('#')) if '#' in cols[i] else tops.append(0)
                    holes = [1 for i in range(0, 190) if pos_board[i] == '#' and pos_board[i + 10] == ' ']
                    val = 0
                    val += a * sum(tops)  # sum col
                    val += b * sum(holes)  # sum holes 
                    val += c * rows.count(10)  # rows cleared
                    val += d * sum([abs(tops[i] - tops[i + 1]) for i in range(0, 9)])  # bumpiness
                    score = val
                    
                    if score > best[1]:
                        best = (pos_board, score)
        if can_move:
            board = best[0]
            rows = [board[i:i + 10].count('#') for i in range(0, 200, 10)]
            if 10 in rows:
                if rows.count(10) == 1:
                    points += 40
                elif rows.count(10) == 2:
                    points += 100
                elif rows.count(10) == 3:
                    points += 300
                else:
                    points += 1200
                for i, v in enumerate(rows):
                    if v == 10:
                        board = '          ' + board[:i * 10] + board[i * 10 + 10:]
        if graphics:
            print("=======================")
            for count in range(20):
                print(' '.join(list(("|" + board[count * 10: (count + 1) * 10] + "|"))), " ", count)
            print("=======================")
            print("score:", points)
        if not can_move:
            return points
    return points

def calculate_fitness(strategy):
    game_scores = 0
    for _ in range(5):
        game_scores += play_game(strategy, False)
    return game_scores / 5

def store_fitness(generation):
    fitness_scores = {}
    avg = 0
    for i, strategy in enumerate(generation):
        fitness_scores[str(strategy)] = calculate_fitness(strategy)
        avg += fitness_scores[str(strategy)]
        print("strategy", i, ":", fitness_scores[str(strategy)])
    return dict(sorted(fitness_scores.items(), key=lambda item: item[1], reverse=True)), avg / POPULATION_SIZE

inp1 = input("(n)ew , or (l)oad previous? ")
gen_cnt = 0

if inp1.lower() == 'l':
    gen_cnt += 1
    filename = input("filename: ")
    stratFile = open(filename, "r").read().split('\n')
    p = []
    fitness_scores = {}
    for strat in stratFile:
        if strat != '':
            tempStrat = strat.split('  ')
            p.append([float(i) for i in tempStrat[0][1:-1].split(', ')])
            fitness_scores[tempStrat[0]] = float(tempStrat[1])
elif inp1.lower() == 'n':
    p = []
    while len(p) != POPULATION_SIZE:
        n = [random.uniform(-0.5, 0.5) for _ in range(4)]
        if n not in p:
            p.append(n)
    fitness_scores, avg = store_fitness(p)
    print("average:", avg)

print("generation #: ", gen_cnt)
print("current best strategy:", list(fitness_scores.keys())[0], " score: ", fitness_scores[list(fitness_scores.keys())[0]])

input_choice = input("(p)lay a game with current best strategy, (s)ave, or (c)ontinue? ")

while input_choice.lower() != 's':
    if input_choice.lower() == 'p':
        play_game([float(i) for i in list(fitness_scores.keys())[0][1:-1].split(', ')], True)
    elif input_choice.lower() == 'c':
        gen_cnt += 1
        next_generation = []
        for child in list(fitness_scores.keys())[:NUM_CLONES]:
            next_generation.append([float(v) for v in child[1:-1].split(', ')])
        while len(next_generation) != POPULATION_SIZE:

            tournament = random.sample(list(fitness_scores.keys()), 2 * TOURNAMENT_SIZE)
            tournament = [(v, fitness_scores[v]) for v in tournament]
            t1 = sorted(tournament[:TOURNAMENT_SIZE], key=lambda item: item[1], reverse=True)
            p1 = t1[-1][0]
            for i in range(TOURNAMENT_SIZE):
                if random.random() < TOURNAMENT_WIN_PROBABILITY:
                    p1 = t1[i][0][1:-1].split(', ')
                    break
            t2 = sorted(tournament[TOURNAMENT_SIZE:], key=lambda item: item[1], reverse=True)
            p2 = t2[-1][0]
            for i in range(TOURNAMENT_SIZE):
                if random.random() < TOURNAMENT_WIN_PROBABILITY:
                    p2 = t2[i][0][1:-1].split(', ')
                    break

            child = []
            randind = random.sample([i for i in range(len(p1))], random.randint(1, len(p1) - 1))
            for i in range(len(p1)):
                child.append(float(p1[i])) if i in randind else child.append(float(p2[i]))

            if random.random() < MUTATION_RATE:
                temp = random.randint(0, len(child) - 1)
                child[temp] += random.uniform(-child[temp], 1 - child[temp])
            if child not in next_generation:
                next_generation.append(child)
        p = next_generation
        
        fitness_scores, avg = store_fitness(p)
        print("avg:", avg)
        print("gen num:", gen_cnt)
        print("best strategy:", list(fitness_scores.keys())[0], " score: ", fitness_scores[list(fitness_scores.keys())[0]])
    
    input_choice = input("(p)lay w best strategy, (s)ave, or (c)ontinue? ")

filename = input("filename: ")  # use a .txt file

with open(filename, "w") as f:
    for strat in list(fitness_scores.keys()):
        f.write(str(strat) + '  ' + str(fitness_scores[strat]) + '\n')

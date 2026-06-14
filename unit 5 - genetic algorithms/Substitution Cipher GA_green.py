import random
from math import log
import sys

frequencyDict = {}
with open('ngrams.txt') as f:
    for line in f:
        ngram, frequency = line.split()
        frequencyDict[ngram] = int(frequency)


POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 25
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 7
MUTATION_RATE = .8


def encodeCipher(message, cipher):
    encoded = ""
    for char in message:
        if char.isalpha():
            index = ord(char) - ord('A')
            encoded += cipher[index]
        else:
            encoded += char
    return encoded


def decodeCipher(message, cipher):
    decoded = ""
    for char in message:
        if char.isalpha():
            index = cipher.index(char)
            decoded += chr(index + ord('A'))
        else:
            decoded += char
    return decoded


def testFitness(n, encoded, cipher):
    decoded = decodeCipher(encoded, cipher)
    nGramsScore = 0
    chunks = [decoded[i: i + n] for i in range(0, len(decoded))]
    for chunk in chunks:
        if chunk in frequencyDict:
            nGramsScore += log(frequencyDict[chunk], 2)
    return nGramsScore


def hillClimbing(encoded):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(alphabet)
    cipher = ''.join(alphabet)
    baseFitness = testFitness(4, encoded, cipher)
    print(decodeCipher(encoded, cipher))
    for _ in range(10):
        random.shuffle(alphabet)
        cipher = ''.join(alphabet)
        fitness = testFitness(4, encoded, cipher)
        if fitness > baseFitness:
            baseFitness = fitness
            print(fitness, decodeCipher(encoded, cipher))
            print('\n')


def generatePopulation():
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    population = []
    for _ in range(POPULATION_SIZE):
        random.shuffle(alphabet)
        population.append(''.join(alphabet))
    return population


def selection(generation, message, genFitness):
    tournamentMembers = random.sample(generation, 2 * TOURNAMENT_SIZE)
    tournamentOne = tournamentMembers[0:TOURNAMENT_SIZE]
    tournamentTwo = tournamentMembers[TOURNAMENT_SIZE: 2 * TOURNAMENT_SIZE]
    t1fitness = {strategy: genFitness[strategy] for strategy in tournamentOne}
    t2fitness = {strategy: genFitness[strategy] for strategy in tournamentTwo}
    t1fitness = sorted(t1fitness.items(), key=lambda x: x[1], reverse=True)
    t2fitness = sorted(t2fitness.items(), key=lambda x: x[1], reverse=True)
    t1parent = t1fitness[0][0] if random.random() < TOURNAMENT_WIN_PROBABILITY else t1fitness[1][0]
    t2parent = t2fitness[0][0] if random.random() < TOURNAMENT_WIN_PROBABILITY else t2fitness[1][0]
    return t1parent, t2parent


def breeding(parents):
    t1parent, t2parent = parents
    parentOne = random.choice(parents)
    if parentOne == t1parent:
        parentTwo = t2parent
    else:
        parentOne = t2parent
        parentTwo = t1parent
    indices = [i for i in range(26)]
    p1CrossIndices = random.sample(indices, CROSSOVER_LOCATIONS)
    child = [''] * 26
    for index in p1CrossIndices:
        child[index] = parentOne[index]
    for letter in parentTwo:
        if letter not in child:
            child[child.index('')] = letter
    if random.random() < MUTATION_RATE:
        swap = random.sample(indices, 2)
        firstLetter = child[swap[0]]
        secondLetter = child[swap[1]]
        child[swap[0]] = secondLetter
        child[swap[1]] = firstLetter
    childCipher = ''.join(child)
    return childCipher
    

message = sys.argv[1]
# message = ''' ZFNNANWJWYBZLKEHBZTNSKDDGJWYLWSBFNSSJWYFNKBGLKOCNKSJEBDWZFNGKLJKJNQFJPFJBXHBZTNRDKNZFNPDEJWYDRPDEGCNZNWJ
# YFZZFLZTCNBBNBZFNNLKZFSLKONWBLCCKJANKBPHGBZFNGNLOBLWSRDCSBZFNRJWLCBFDKNJWLWSWDTDSUWDTDSUOWDQBQFLZBYDJWYZ
# DFLGGNWZDLWUTDSUTNBJSNBZFNRDKCDKWKLYBDRYKDQJWYDCSJZFJWODRSNLWEDKJLKZUJNANWZFJWODRDCSSNLWEDKJLKZUZFNRLZFN
# KQNWNANKRDHWSJZFJWODRSNLWEDKJLKZU'''
gen = generatePopulation()
genFitness = {}
for strategy in gen:
    fitness = testFitness(4, message, strategy)
    genFitness[strategy] = fitness
x = 0
while x < 500:
    nextGen = []
    ranks = sorted(genFitness.items(), key=lambda x: x[1], reverse=True)
    for i in range(NUM_CLONES):
        nextGen.append(ranks[i][0])
    while len(nextGen) < POPULATION_SIZE:
        child = breeding(selection(gen, message, genFitness))
        if child not in nextGen:
            nextGen.append(child)
    nextGenFitness = {}
    for strategy in nextGen:
        fitness = testFitness(4, message, strategy)
        nextGenFitness[strategy] = fitness
    gen = nextGen
    genFitness = nextGenFitness
    ranks = sorted(genFitness.items(), key=lambda x: x[1], reverse=True)
    bestStrategy = ranks[0][0]
    print(decodeCipher(message, bestStrategy))
    print('\n')
    x += 1


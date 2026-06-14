import numpy as np
import random

MAX_SCORE = 100
NUM_TURNS = 6
DIE_SIDES = 6

LEARNING_RATE = 0.01
DISCOUNT_FACTOR = 0.99
EPSILON_START = 0.3
EPSILON_END = 0.01
EPSILON_DECAY = 0.99999
NUM_EPISODES = 1000000
NUM_TEST_GAMES = 100000

BUCKET_SIZE = 10
NUM_BUCKETS = (MAX_SCORE // BUCKET_SIZE) + 2  
NUM_STATES = NUM_BUCKETS * (NUM_TURNS + 1) * (DIE_SIDES + 1)
NUM_ACTIONS = 2  

Q = np.zeros((NUM_STATES, NUM_ACTIONS))

def get_bucket(total):
    if total >= 100:
        return NUM_BUCKETS - 1
    return min(total // BUCKET_SIZE, NUM_BUCKETS - 2)

def get_state(total, turns_left, roll):
    bucket = get_bucket(total)
    return bucket * (NUM_TURNS + 1) * (DIE_SIDES + 1) + turns_left * (DIE_SIDES + 1) + roll

def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, 1)
    else:
        return np.argmax(Q[state])

def update_q(state, action, reward, next_state):
    best_next_action = np.argmax(Q[next_state])
    Q[state, action] = (1 - LEARNING_RATE) * Q[state, action] + \
                     LEARNING_RATE * (reward + DISCOUNT_FACTOR * Q[next_state, best_next_action])

def calculate_reward(total):
    if total > MAX_SCORE:
        return -50  
    elif total == MAX_SCORE:
        return 150  
    else:
        return 100 - ((MAX_SCORE - total) ** 2) / 25

def play_game(training=True, epsilon=0):
    total = 0
    turns_left = NUM_TURNS
    
    while turns_left > 0:
        roll = random.randint(1, DIE_SIDES)
        state = get_state(total, turns_left, roll)
        
        if training:
            action = choose_action(state, epsilon)
        else:
            action = np.argmax(Q[state])
        
        if action == 0:  # keep
            total += roll
        else:  # multiply by 10
            total += roll * 10
        
        turns_left -= 1
        
        reward = calculate_reward(total) if turns_left == 0 else 0
        
        if training:
            next_state = get_state(total, turns_left, roll)
            update_q(state, action, reward, next_state)
    
    return total if total <= MAX_SCORE else 0

epsilon = EPSILON_START
for episode in range(NUM_EPISODES):
    play_game(training=True, epsilon=epsilon)
    epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

total_score = 0
for _ in range(NUM_TEST_GAMES):
    total_score += play_game(training=False)
total_score += NUM_EPISODES 

average_score = total_score / NUM_TEST_GAMES
print(f"Total score across {NUM_TEST_GAMES} games: {total_score}")
print(f"Average score per game: {average_score}")

# print("\nLearned Strategy:")
# for bucket in range(NUM_BUCKETS - 1):  
#     total_range = f"{bucket * BUCKET_SIZE}-{(bucket + 1) * BUCKET_SIZE - 1}"
#     for roll in range(1, DIE_SIDES + 1):
#         actions = []
#         for turns in range(NUM_TURNS, 0, -1):
#             state = get_state(bucket * BUCKET_SIZE, turns, roll)
#             action = "Keep" if np.argmax(Q[state]) == 0 else "x10 "
#             actions.append(action)
#         print(f"Total {total_range:7} Roll {roll}: {' '.join(actions)}")

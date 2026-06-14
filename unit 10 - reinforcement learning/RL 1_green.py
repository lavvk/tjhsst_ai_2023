import random
import math

def choose_bandit(bandits, policy, q_vals, counts):
    if policy == "random":
        return random.randint(0, len(bandits) - 1)
    elif policy == "greedy":
        return max(range(len(bandits)), key=lambda i: q_vals[i])
    elif policy == "greedy_ucb":
        total_counts = sum(counts)
        if total_counts > 0:
            ucb_vals = [q_vals[i] + math.sqrt(2 * math.log(total_counts) / (counts[i] + 1e-10)) for i in range(len(bandits))]
            return max(range(len(bandits)), key=lambda i: ucb_vals[i])
        else:
            return random.randint(0, len(bandits) - 1)
    elif policy == "epsilon_greedy_ucb":
        total_counts = sum(counts)
        if random.random() < 0.1:
            return random.randint(0, len(bandits) - 1)
        else:
            if total_counts > 0:
                ucb_vals = [q_vals[i] + math.sqrt(2 * math.log(total_counts) / (counts[i] + 1e-10)) for i in range(len(bandits))]
                return max(range(len(bandits)), key=lambda i: ucb_vals[i])
            else:
                return random.randint(0, len(bandits) - 1)
    elif policy.startswith("epsilon_"):
        epsilon = float(policy.split("_")[1])
        if random.random() < epsilon:
            return random.randint(0, len(bandits) - 1)
        else:
            return max(range(len(bandits)), key=lambda i: q_vals[i])

def evaluate_policy(bandits, policy, n_games, n_moves):
    scores = []
    for _ in range(n_games):
        q_vals, counts, total_score = [0.0] * len(bandits), [0] * len(bandits), 0.0
        for _ in range(n_moves):
            chosen = choose_bandit(bandits, policy, q_vals, counts)
            reward = random.normalvariate(bandits[chosen], 1.0)
            q_vals[chosen] = (q_vals[chosen] * counts[chosen] + reward) / (counts[chosen] + 1)
            counts[chosen] += 1
            total_score += reward
        scores.append(total_score)
    return sum(scores) / n_games

n_bandits, n_games, n_moves = 10, 200, 2000
bandits = [random.normalvariate(0, 1) for _ in range(n_bandits)]
ideal_score = n_moves * max(bandits)
policies = ["random", "greedy", "greedy_ucb", "epsilon_0.001", "epsilon_0.01", "epsilon_0.1", "epsilon_0.5", "epsilon_1.0", "epsilon_greedy_ucb"]
results = [(policy, evaluate_policy(bandits, policy, n_games, n_moves)) for policy in policies]
for policy, score in results:
    print(f"{policy}: {score:.2f}")
print(f"Ideal score: {ideal_score:.2f}")


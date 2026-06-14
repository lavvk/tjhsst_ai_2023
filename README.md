# AI Course Projects

Solutions to a my high school Artificial Intelligence course taught by former teacher at TJHSST, Mr. Malcolm Eckel. The course has content spanning classic search through modern deep learning. Each unit folder contains my submitted
solution(s) alongside the original assignment prompt(s).

## Difficulty tiers

Assignments were offered at four ascending difficulty tiers. Each solution file is suffixed with
the tier it satisfies (e.g. `Sudoku_red.py`).

| Tier | Meaning |
|------|---------|
| `green` | Core / foundational version |
| `blue`  | Standard version |
| `red`   | Advanced version |
| `black`  | Hardest / extension version |

## Contents

| Unit | Topic | Assignments completed (tier) |
|------|-------|------------------------------|
| [0](unit%200%20-%20python) | Python | Project Euler (red), Python Basics, Data Structures (black) |
| [1a](unit%201a%20-%20uninformed%20search) | Uninformed search | Sliding Puzzle Model (green), BFS (green), Bidirectional BFS (red), Iterative Deepening DFS (red), Peg Solitaire (black), Word Ladders (blue) |
| [1b](unit%201b%20-%20informed%20search) | Informed search | A\* Sliding Puzzle (blue) |
| [2](unit%202%20-%20constraint%20satisfaction) | Constraint satisfaction | N-Queens (green), N-Queens Incremental (blue), Sudoku (blue, red) |
| [3](unit%203%20-%20turn%20based%20games) | Turn-based games | Tic-Tac-Toe (green), Ghost (blue), Othello (blue, red) |
| [5](unit%205%20-%20genetic%20algorithms) | Genetic algorithms | Substitution Cipher (green), Tetris (blue, red) |
| [6](unit%206%20-%20unsupervised%20learning) | Unsupervised learning | K-Means Clustering (green), Image K-Means (blue, red) |
| [7](unit%207%20-%20supervised%20learning) | Supervised learning | Decision Trees (red) |
| [8](unit%208%20-%20neural%20networks) | Neural networks | Gradient Descent (green), Perceptrons 1–4 (green), Back Propagation (blue), Perceptrons Graph (blue), MNIST (blue, red) |
| [9](unit%209%20-%20RNNs%20and%20generative%20AI) | RNNs & generative AI | RNNs (blue), Generative AI (red) |
| [10](unit%2010%20-%20reinforcement%20learning) | Reinforcement learning | Multi-Armed Bandit (green), Grid-World Q-Learning (blue), Game101 (red) |
| [DP](dynamic%20programming) | Dynamic programming | Memoization & optimization problems |
| [Final](final%20project%20-%20train%20routes) | Final project | North American train-route planner (green CLI, blue GUI) |

## Running the code

Each unit folder is self-contained: the solution scripts read their data (CSV / TXT / PKL / images)
from co-located files, so run a script from inside its folder. Some scripts depend on common
scientific-Python packages (`numpy`, `scipy`, `matplotlib`, `Pillow`).

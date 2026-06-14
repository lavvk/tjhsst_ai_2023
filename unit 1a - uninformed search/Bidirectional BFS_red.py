from collections import deque
from time import perf_counter
import sys

def get_children(size, string):
    directions = [-1, 1, size, -size]
    children = []

    idx = string.index('.')
    for move in directions:
        change = int((idx + move) / size) - int(idx / size)
        if ((idx + move >= 0)and (idx + move < len(string))and (abs(change) <= abs(int(move / size)))):
            curr = (string[: idx + move]+ string[idx]+ string[idx + move + 1 :])
            curr = curr[: idx] + string[idx + move] + curr[idx + 1 :]
            children.append(curr)
    return children

def bfs(string): ## same from other lab
    fringe = deque([[string, [string]]])
    visited = set([string])
    length = int(len(string) ** 0.5)

    goal_string = ''.join(sorted(string.replace('.', ''))) + '.'

    while len(fringe) != 0:
        v = fringe.popleft()
        if v[0] == goal_string:
            return len(v[1]) - 1
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

def bibfs(string):
    fringe = deque([[string, 0]])
    dict = {string: 0}
    visited = set([string])

    goal = ''.join(sorted(string.replace('.', ''))) + '.'
    other_fringe = deque([[goal, 0]])
    other_dict = {goal: 0}
    other_visited = set([goal])
    length = int(len(string) ** (1 / 2))

    while len(fringe) != 0 and len(other_fringe) != 0:
        v = fringe.popleft()
        if v[0] == goal:
            return v[1]
        elif v[0] in other_dict:
            return v[1] + other_dict[v[0]]
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + 1])
                dict[c] = v[1] + 1

        v = other_fringe.popleft()
        if v[0] == string:
            return v[1]
        elif v[0] in dict:
            return v[1] + dict[v[0]]
        for c in get_children(length, v[0]):
            if c not in other_visited:
                other_visited.add(c)
                other_fringe.append([c, v[1] + 1])
                other_dict[c] = v[1] + 1
    return None

with open(sys.argv[1], "r") as f:
    line_list = [line.strip() for line in f]

    for i, puzzle in enumerate(line_list):
        start_time = perf_counter()
        data = puzzle.split()
        puzzle_input = data[1]
        solution = bfs(puzzle_input)
        end_time = perf_counter()
        if solution is not None:
            print("bfs time::   Line " + str(i) + ": " + puzzle_input + ", " + str(solution) + " moves found in " + str(end_time - start_time) + " seconds")
        else:
            print("bfs time::   Line " + str(i) + ": " + puzzle_input + " No solution found")
        
        start_time = perf_counter()
        data = puzzle.split()
        puzzle_input = data[1]
        solution = bibfs(puzzle_input)
        end_time = perf_counter()
        if solution is not None:
            print("bibfs time:: Line " + str(i) + ": " + puzzle_input + ", " + str(solution) + " moves found in " + str(end_time - start_time) + " seconds")
        else:
            print("bibfs time:: Line " + str(i) + ": " + puzzle_input + " No solution found")


'''
responses for bibfs (unit 1a red1) 

1) Return to the benchmark you did for question 5 on Sliding Puzzles: BFS using the 4x4_puzzles.txt file. Repeat the exercise using Bidirectional BFS. What’s the last puzzle you can solve in less than a minute? How does this compare to your BFS results?

I can run up to line 41 which is at 41 seconds. In normal BFS, I can go till line 21 then it times out.  

2) Return Word Ladders, and this time find all of the ladders using Bidirectional BFS instead of BFS. Find the total runtime for the whole sample puzzle file using each strategy. What speed gains did you get?


There was not that much gains with time (0.01 of a second) 
for BFS algo time was :: Time to solve all puzzles was:  0.18447945901425555  seconds
For BiBFS algo time was :: Time to solve all puzzles was:  0.1788701660116203  seconds


3) How did you store the word ladder during BiBFS, not just the length? Send me code & an explanation.

In the bibfs function, I modified it to store the actual word ladder (sequence of words) rather than just the length. I changed the function to keep track of the forward and backward paths separately and concatenate them when the intersection is found. 

code
```
def bibfs(string, goal, children, word_set):
    forward_fringe = deque([[string, [string]]])
    backward_fringe = deque([[goal, [goal]]])
    
    forward_visited = set([string])
    backward_visited = set([goal])
    
    while forward_fringe and backward_fringe:
        forward_node = forward_fringe.popleft()
        backward_node = backward_fringe.popleft()
        
        forward_word = forward_node[0]
        backward_word = backward_node[0]
        
        if forward_word in backward_visited:
            intersection = forward_word
            forward_path = forward_node[1]
            backward_path = backward_node[1][::-1]
            return forward_path + backward_path
            
        for forward_child in children[forward_word]:
            if forward_child not in forward_visited:
                forward_visited.add(forward_child)
                forward_fringe.append([forward_child, forward_node[1] + [forward_child]])
                
        for backward_child in children[backward_word]:
            if backward_child not in backward_visited:
                backward_visited.add(backward_child)
                backward_fringe.append([backward_child, backward_node[1] + [backward_child]])
                
    return None


Explanation:

The forward_node[1] represents the path taken from the start word to the current forward word.
The backward_node[1] represents the path taken from the goal word to the current backward word.
When the intersection is found (i.e., forward_word is in backward_visited), it means that the forward and backward searches have met. At this point, the function concatenates the forward and backward paths to form the complete word ladder.
The returned result is a list containing the sequence of words in the word ladder.
With this modification, the bibfs function now returns the actual word ladder, not just the length of the ladder.


4) Finally, from your results in 1, 2, and 3, and your own judgment & common sense, explain where Bidirectional
BFS is most useful as an alternative to BFS.


Bidirectional BFS is faster when you're looking for something in a big space like in word ladders when we worked w a whole dictionary, and you have an idea of where it might be. 
Instead of searching from just one end, it goes from both the starting point and the destination at the same time, making things quicker when the two paths meet. 
It's like having two friends looking for lost keys - one starts at the door, and the other starts where the keys might be, and they meet in the middle.

'''

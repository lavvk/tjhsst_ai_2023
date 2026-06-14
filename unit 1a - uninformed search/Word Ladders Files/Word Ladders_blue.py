import sys
from collections import deque
from time import perf_counter

def get_children(word_set):
    children = {}
    letters = 'abcdefghijklmnopqrstuvwxyz'
    
    for word in word_set:
        words = []
        for idx in range(len(word)):
            for letter in letters:
                if word[idx] != letter:
                    new_word = word[:idx] + letter + word[idx+1:]
                    if new_word in word_set:
                        words.append(new_word)
        children[word] = words
    return children

def BFS(string, goal, children, word_set):
    fringe = deque([[string, [string]]])
    visited = set([string])
    
    while fringe:
        v = fringe.popleft()
        if v[0] == goal:
            return v[1]
        for c in children[v[0]]:
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None 

def brainteaser_1(children, word_set):
    count = 0
    for word in word_set:
        if not children[word]:
            count += 1
    return count

def brainteaser_2(children, dict):
    clump = 0
    for string in dict:
        fringe = deque([[string, [string]]])
        visited = set([string])

        while len(fringe)!=0:
            v = fringe.popleft()
            for c in children[v[0]]:
                if c not in visited:
                    visited.add(c)
                    fringe.append([c, v[1] + [c]])
        clump = max(clump, len(visited))
    return clump

def brainteaser_3(children, word_set):
    count = 0
    nodes = list(word_set)

    while nodes:
        start_node = nodes[0]
        fringe = deque([[start_node, 0]])
        visited = set([start_node])

        while fringe:
            current_node, depth = fringe.popleft()
            nodes.remove(current_node)

            for neighbor in children[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    fringe.append([neighbor, depth + 1])

        if len(visited) > 1:
            count += 1

    return count


def brainteaser_4(children, word_set):
    longest_path = []
    
    for start_word in word_set:
        fringe = deque([[start_word, [start_word]]])
        visited = set([start_word])

        while fringe:
            current_node, path_so_far = fringe.popleft()

            for next_node in children[current_node]:
                if next_node not in visited:
                    visited.add(next_node)
                    new_path = path_so_far + [next_node]
                    fringe.append([next_node, new_path])

                    # update the longest path if a longer one is found
                    if len(new_path) > len(longest_path):
                        longest_path = new_path

    return longest_path


start = perf_counter()
with open(sys.argv[1], "r") as f:
    word_set = {line.strip() for line in f}
end = perf_counter()
print("Time to create the data structure was: " + str(end - start) + " seconds\n")

start = perf_counter()

children = get_children(word_set)
with open(sys.argv[2], "r") as f:
    idx = 0
    for line in f:
        temp = line.split()
        result = BFS(temp[1], temp[0], children, word_set)
        if result is None:
            print("Line: " + str(idx) + "\nNo solution!\n")
        else:
            print("Line: " + str(idx) + "\nLength is: " + str(len(result)) + "\n" + "\n".join(reversed(result)) + "\n")
        idx += 1

end = perf_counter()
print("Time to solve all puzzles was: " ,(end - start) , " seconds")

start = perf_counter()
singletons_count = brainteaser_1(children, word_set)
biggest_subcomponent = brainteaser_2(children, word_set)
clumps_count = brainteaser_3(children, word_set)
print("\n1) There are " + str(singletons_count) + " singletons.")
print("2) The biggest subcomponent has " + str(biggest_subcomponent) + " words.")
print("3) There are " + str(clumps_count) + " 'clumps' (subgraphs with at least two words).")
print("Questions 1-3 answered in " + str(perf_counter() - start) + " seconds.\n")


start = perf_counter()
result = brainteaser_4(children, word_set)
print("4) The longest path is:", "[['",result[0],"', '",result[-1],"']",len(result),"]")
print("Length is:", len(result))
print("\n".join(result))
print("Time to solve all puzzles was:", perf_counter() - start, "seconds")
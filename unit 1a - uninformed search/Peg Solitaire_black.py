from collections import deque
# from time import perf_counter
import sys
matrixstr= ""
goal=""
for i in range(15):
    if(i == int(sys.argv[1])):
        matrixstr += "0"
        goal += "1"
    else:
        matrixstr += "1"
        goal += "0"

possiblities = possible_moves = [(3, 4, 5), (6, 7,8), (7, 8, 9), (10, 11, 12), (11, 12,13), 
                                       (12,13,14), (0,1,3), (1,3,6),(3,6,10), (0, 2, 5), (2, 5, 9), 
                                       (5, 9, 14), (2, 4, 7), (4, 7, 11), (5, 8, 12), (1, 4, 8), (4, 8, 13), (3,7,12)]
def get_children(node):
    matrix = list(node)
    results = []
    for pairs in possiblities:
        one, two, three = pairs

        if(matrix[one] == "0" and matrix[two] == "1" and matrix[three] == "1"):
            updated_matrix = list(matrix)
            updated_matrix[one] = "1"
            updated_matrix[two] = "0"
            updated_matrix[three] = "0"
            results.append(''.join(updated_matrix))
        elif(matrix[one] == "1" and matrix[two] == "1" and matrix[three] == "0"):
            updated_matrix = list(matrix)
            updated_matrix[one] = "0"
            updated_matrix[two] = "0"
            updated_matrix[three] = "1"
            results.append(''.join(updated_matrix))
    return results

def dfs(start, goalstate):
    fringe = deque()
    visited = set()
    fringe.append((start, [start]))
    visited.add(start)
    count = 0
    while fringe:
        count +=1
        node, pastmoves = fringe.pop()
        if(node == goalstate):
            return pastmoves, len(pastmoves)
        else:
            for child in get_children(node):
                if child not in visited:
                    updatedpath = pastmoves + [child]
                    fringe.append((child, updatedpath))
                    visited.add(child)
    return [], -1
listofgrids = dfs(matrixstr, goal)

def format_string(gridlist):
    for lists in gridlist:
        print(format_triangle(str(lists)))
def format_triangle(input_str):
    formatted_string = ""
    max_width = len(input_str)
    matrix_length = 1
    matrix_start = 0
    num_spaces = 5
    while matrix_start < max_width:
        matrix_end = matrix_start + matrix_length
        line = input_str[matrix_start:matrix_end]
        formatted_string += " " * (num_spaces)
        for letter in line: 
            if letter == "1":
                formatted_string +=  "1 "
            else:
                formatted_string += "0 "
        num_spaces -=1
        formatted_string += "\n"
        matrix_length += 1  
        matrix_start = matrix_end
    return formatted_string
format_string(listofgrids[0])
print(listofgrids[1]-1) 

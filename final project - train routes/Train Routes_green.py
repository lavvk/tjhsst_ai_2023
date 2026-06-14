import sys
from time import perf_counter
from heapq import heappush, heappop
from math import pi, acos, sin, cos

start_time = perf_counter()

coordinates = {}
junctions = {}
junct_id = {}

def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

with open("rrNodeCity.txt") as f:
    for line in f:
        node_id = line.split()[0]
        junct_name = line.split()[1] if len(line.split()) == 2 else line.split()[1] + " " + line.split()[2]
        junct_id[junct_name] = node_id

with open("rrNodes.txt") as f:
    for line in f:
        node = line.split()[0]
        coord = (float(line.split()[1]), float(line.split()[2]))
        coordinates[node] = coord

with open("rrEdges.txt") as f:
    for line in f:
        junct_1, junct_2 = line.split()[0], line.split()[1]
        distance = calcd(coordinates[junct_1], coordinates[junct_2])

        if junct_1 not in junctions:
            junctions[junct_1] = set()
        junctions[junct_1].add((junct_2, distance))

        if junct_2 not in junctions:
            junctions[junct_2] = set()
        junctions[junct_2].add((junct_1, distance))

end_time = perf_counter()

# old a_star::
    
# def a_star(string):
#     closed = set()
#     fringe = []
#     start_node = (heuristic(string), string, 0)
#     heappush(fringe, start_node)
#     length = int(len(string)**(0.5))

#     while len(fringe)!=0:
#         v = heappop(fringe)
#         if v[1]==goal_test(string):
#             return v[2]
#         if v[1] not in closed:
#             closed.add(v[1])
#             for child in get_children(length, v[1]):
#                 if child not in closed:
#                     temp = (v[2]+1+heuristic(child), child, v[2]+1)
#                     heappush(fringe, temp)
#     return None

def dijkstra(junct_start, junct_end):
    start_id, end_id = junct_id[junct_start], junct_id[junct_end]
    closed = set()
    start = (0, start_id)
    fringe = []
    heappush(fringe, start)

    while fringe:
        v = heappop(fringe)
        if v[1] == end_id:
            return v[0]
        if v[1] not in closed:
            closed.add(v[1])
            for child in junctions[v[1]]:
                if child[0] not in closed:
                    temp = (v[0] + child[1], child[0])
                    heappush(fringe, temp)
    return None

def a_star(junct_start, junct_end):
    start_id, end_id = junct_id[junct_start], junct_id[junct_end]
    closed = set()
    start = (calcd(coordinates[start_id], coordinates[end_id]), 0, start_id)
    fringe = []
    heappush(fringe, start)

    while fringe:
        v = heappop(fringe)
        if v[2] == end_id:
            return v[1]
        if v[2] not in closed:
            closed.add(v[2])
            for child in junctions[v[2]]:
                if child not in closed:
                    temp = ( calcd(coordinates[child[0]], coordinates[end_id]) + v[1]+ child[1],v[1] + child[1],child[0],)
                    heappush(fringe, temp)
    return None

print("Time to create data structure:", end_time - start_time)


dij_start = perf_counter()
dij_dist = dijkstra(sys.argv[1], sys.argv[2])
dij_end = perf_counter()

star_start = perf_counter()
star_dist = a_star(sys.argv[1], sys.argv[2])
star_end = perf_counter()


print(sys.argv[1], "to" , sys.argv[2], "with Dijkstra:" , str(dij_dist) , "in", str(dij_end - dij_start) , "seconds")
print(sys.argv[1], "to", sys.argv[2], "with A*:" , str(star_dist) ,"in" , str(star_end - star_start) , "seconds")



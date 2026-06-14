import tkinter as tk
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



line_data = {}

def create_grid(canvas, c, j):
    for start_junction, edges in j.items():
        for end_junction, _ in edges:
            start_x = c[start_junction][1] * 15 + 2050
            start_y = c[start_junction][0] * -15 + 950
            end_x = c[end_junction][1] * 15 + 2050
            end_y = c[end_junction][0] * -15 + 950

            line_data[(start_junction, end_junction)] = canvas.create_line([(start_x, start_y), (end_x, end_y)], tag='grid_line')

root = tk.Tk()

canvas = tk.Canvas(root, height=800, width=1200, bg='white')
create_grid(canvas, coordinates, junctions)
canvas.pack(expand=True)

def run_algorithm(start, end, algorithm):
    algorithm_name = algorithm.__name__
    result = algorithm(start, end)
    if result:
        path = result[2] if algorithm_name == 'dijkstra' else result[3]
        for count in range(1, len(path)):
            edge_key = (path[count-1], path[count])
            if edge_key in line_data.keys():
                canvas.itemconfig(line_data[edge_key], fill="green", width = 2.5)
            else:
                canvas.itemconfig(line_data[(path[count], path[count-1])], fill="green", width = 2.5)
            root.update()

        canvas.delete("all")
        create_grid(canvas, coordinates, junctions)

def dijkstra(junct_start, junct_end):
    start_id, end_id = junct_id[junct_start], junct_id[junct_end]
    closed = set()
    fringe = []
    count = 1
    heappush(fringe, (0, start_id, (start_id, )))
    
    while fringe:
        v = heappop(fringe)
        if v[1] == end_id:
            return v
        if v[1] not in closed:
            closed.add(v[1])
            for c, distance in junctions[v[1]]:
                temp = (v[0] + distance, c, v[2] + (c, ))
                heappush(fringe, temp)

                edge_key = (v[1], c)
                if edge_key in line_data.keys():
                    canvas.itemconfig(line_data[edge_key], fill="red", width = 1.5)
                    count += 1
                else:
                    canvas.itemconfig(line_data[(c, v[1])], fill="red", width = 1.5)
                    count += 1
        if count % 1000 == 0:
            root.update()
    return None

def a_star(junct_start, junct_end):
    start_id, end_id = junct_id[junct_start], junct_id[junct_end]
    closed = set()
    fringe = []
    count = 1
    heappush(fringe, (calcd(coordinates[start_id], coordinates[end_id]), 0, start_id, (start_id, )))
    
    while fringe:
        v = heappop(fringe)
        if v[2] == end_id:
            return v
        if v[2] not in closed:
            closed.add(v[2])
            for c, distance in junctions[v[2]]:
                temp = (calcd(coordinates[c], coordinates[end_id]) + v[1] + distance, v[1] +distance, c, v[3] + (c, ))
                heappush(fringe, temp)

                edge_key = (v[2], c)
                if edge_key in line_data.keys():
                    canvas.itemconfig(line_data[edge_key], fill="blue", width=1.5)
                    count += 1
                else:
                    canvas.itemconfig(line_data[(c, v[2])], fill="blue", width=1.5)
                    count += 1
        if count % 1000 == 0:
            root.update()
    return None

run_algorithm(sys.argv[1], sys.argv[2], dijkstra)
run_algorithm(sys.argv[1], sys.argv[2], a_star)

root.mainloop()

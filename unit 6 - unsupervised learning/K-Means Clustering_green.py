import math
import random
import sys

orig_datalist = []

with open("star_data.csv") as f:
    for line in f:
        x = line.strip().split(",")
        orig_datalist.append(tuple(x[0:5]))
orig_datalist.pop(0)

linearized_datalist = []

for data_tuple in orig_datalist:
    to_add = []  
    for index, item in enumerate(data_tuple):
        item = float(item) 
        if index == 0:
            to_add.append(math.log(item))  
        elif index != 3 and index != 4:  
            new_item = math.log(item)  
            to_add.append(new_item)
        else:
            to_add.append(item) 
    linearized_datalist.append(tuple(to_add))

# idx1= int(sys.argv[1])
# idx2= int(sys.argv[2])
# idx3= int(sys.argv[3])
# idx4= int(sys.argv[4])
# idx5= int(sys.argv[5])
# idx6= int(sys.argv[6])

def distance(point1, point2):
    return math.sqrt(sum((point1[i] - point2[i]) ** 2 for i in range(len(point1))))

def avg(values):
    if not values:
        return []
    num_dimensions = len(values[0])
    return [sum(values[j][i] for j in range(len(values))) / len(values) for i in range(num_dimensions)]

def kmeans(data, k):
    means = random.sample(data, k)  
    # means = [data[idx1],data[idx2],data[idx3],data[idx4],data[idx5],data[idx6]]

    iterations = 0
    while True:
        clusters = [[] for _ in range(k)]
        for point in data:
            distances = [distance(point[:-1], mean[:-1]) for mean in means]
            closest_mean_index = distances.index(min(distances))
            clusters[closest_mean_index].append(point)
        
        new_means = [avg(cluster) for cluster in clusters]
        max_distance = max(distance(means[i][:-1], new_means[i]) for i in range(k))
        
        if max_distance < 1e-6:  # convergence check
            break
        means = new_means
        iterations += 1
    
    return means, clusters, iterations

k = 8
means, clusters, iterations = kmeans(linearized_datalist, k)



for i, mean in enumerate(means):
    last_elem = float(round(mean[-1]))
    rounded_mean = mean[:-1] + [last_elem]
    print("Star Type", i+1, ":", rounded_mean[-1])
    print("Mean", i + 1, ":", rounded_mean)
    print("Cluster", i + 1, ":", clusters[i],"\n")
print("Total number of iterations:", iterations)


from time import perf_counter
start = perf_counter()
import sys
from heapq import heappush, heappop

#All your code goes here, including reading in the files and printing your output


f1, f2, f3 = sys.argv[1], sys.argv[2], sys.argv[3] 
with open(f1) as f:
    list1 = [int(line.strip()) for line in f]
with open(f2) as f:
    list2 = [int(line.strip()) for line in f]
with open(f3) as f:
    list3 = [int(line.strip()) for line in f]


#1
count = 0
set1 = set(list1)  # First text file to set
set2 = set(list2)  # 2nd text file to set
for val in set1:
    if val in set2:
        count += 1
print("1:", count)

#2
sum_vals = 0
unique_count = 0
xset = set()
for val in list1:
    if val not in xset:
        unique_count += 1
        xset.add(val)
        if unique_count % 100 == 0:
            sum_vals += val
print("2:", sum_vals)

#3

count = 0
dict1 = {}  # Making a dictionary for the first file
for x in list1:
    if x in dict1:
        dict1[x] += 1
    else:
        dict1[x] = 1
dict2 = {}  # Making a dictionary for the second file
for x in list2:
    if x in dict2:
        dict2[x] += 1
    else:
        dict2[x] = 1
set3 = set(list3)  # Third set for file 3

for i in set3:  # Actual logic applied
    if i in dict1:
        count += dict1[i]
    if i in dict2:
        count += dict2[i]
print("3:", count)

#4
z = list(set1)
z.sort()
print("4:", z[:10])


#5
n = sorted(set2)[-10:]
n.reverse()
print("5:", n)

#6
rn = 0
total = set()
heap = []

for i, val in enumerate(list1):
    heappush(heap, val)

    if val % 53 == 0:
        rn = i

        x = 0

        while heap[x] in total:
            heappop(heap)

        total.add(heap[x])

print("6:", sum(total))



end = perf_counter()
print("Total time:", end - start)      


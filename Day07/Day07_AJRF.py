import numpy as np

#input_txt = "16,1,2,0,4,2,7,1,2,14"
with open("Day07/input_AJRF.txt") as f:
    input_txt = f.readline()

inputs = input_txt.split(",")
inputs = np.array(inputs, dtype = "int")

# Brute force it
def abs_dist(x, y):
    return(abs(x-y))

total_dist = [np.sum([abs_dist(pos, i) for i in inputs]) for pos in np.arange(min(inputs), max(inputs) + 1)]
print("Minimum distance:", min(total_dist))

# Part 2
def distance_cost(x, y):
    dist = abs(x-y)
    # cost for dist n = (1 + 2 + ... + n)  Use the classic Gauss method to sum them: (n+1) * n / 2
    dist_cost = int((dist + 1) * dist / 2)
    return(dist_cost)

total_dist_cost = [np.sum([distance_cost(pos, i) for i in inputs]) for pos in np.arange(min(inputs), max(inputs) + 1)]
print("Minimum distance cost:", min(total_dist_cost))


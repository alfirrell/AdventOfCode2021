import numpy as np
#import pandas as pd
from queue import PriorityQueue

# Read data
with open("Day15/input_AJRF.txt", "r") as f:
    input = f.readlines()

input_mat = np.array([list(line.strip()) for line in input], dtype="int")
input_mat

# Helper functions
def get_neighbours(mat, current_loc):
    neighbours = []
    for next_loc in current_loc + np.array([[0,1], [1,0], [-1,0], [0,-1]]):
        if next_loc[0]>=0 and next_loc[0] < n_rows and \
            next_loc[1]>=0 and next_loc[1] < n_cols:
            neighbours.append([next_loc, mat[next_loc[0], next_loc[1]]])

    return(neighbours)

def coord_to_int(coord_tuple):
    return(coord_tuple[0]*n_cols + coord_tuple[1])

def int_to_coord(i):
    col = i % n_cols
    row = i // n_cols
    return np.array([row, col])

# TODO: this calcs all points - could put in a stop when reach the end target
def dijkstra(mat, start_location, end_location):

    costs_from_start = {coord_to_int((i,j)): float("inf") for i in np.arange(mat.shape[0]) for j in np.arange(mat.shape[1]) }
    costs_from_start[coord_to_int(start_location)] = 0

    start_loc_int = coord_to_int(start_location)
    end_loc_int = coord_to_int(end_location)

    visited_locs = []

    pq = PriorityQueue()
    pq.put((0, start_loc_int)) ## put in the start point with distance zero

    count = 0
    while not pq.empty():
        count += 1
        if count % 1000 == 0:
            print(max(visited_locs))

        (_, current_loc_int) = pq.get()
        visited_locs.append(current_loc_int)
        current_loc = int_to_coord(current_loc_int)

        if current_loc_int == end_loc_int:
            break

        neighbours = get_neighbours(mat, current_loc)
        # print(neighbours)
        for neighbour in neighbours:
            neighbour_loc = neighbour[0]
            neighbour_loc_int = coord_to_int(neighbour_loc)

            distance = neighbour[1] #dist(current_loc, neighbour_loc)
            if not(neighbour_loc_int in visited_locs):
                prev_cost = costs_from_start[neighbour_loc_int]
                new_cost = costs_from_start[current_loc_int] + distance
                if new_cost < prev_cost:
                    ## Add to the priority queue
                    pq.put((new_cost, neighbour_loc_int))
                    costs_from_start[neighbour_loc_int] = new_cost
        # print(costs_from_start)
        # print(visited_locs)

    return costs_from_start

# Run algo
start_location = np.array([0,0])
n_rows, n_cols = input_mat.shape
end_location = np.array([n_rows-1, n_cols-1])

costs = dijkstra(input_mat, start_location, end_location)
print("Cost to end:", costs[coord_to_int(end_location)])

## Part 2
# construct the extend matrix
mats = []
for i in np.arange(5):
    mat_cols = []
    for j in np.arange(5):
        mat_cols.append((input_mat + i + j - 1) % 9 + 1)
    mat_wide = np.concatenate(mat_cols, axis = 1)
    mats.append(mat_wide)

big_mat = np.concatenate(mats, axis = 0)
#big_mat.shape

# Run algo on big mat
# THIS IS REALLY SLOW! Could do better...
start_location = np.array([0,0])
n_rows, n_cols = big_mat.shape
end_location = np.array([n_rows-1, n_cols-1])
#end_location

costs = dijkstra(big_mat, start_location, end_location)
print("Cost to end:", costs[coord_to_int(end_location)])

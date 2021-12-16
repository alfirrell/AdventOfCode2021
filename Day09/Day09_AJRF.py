import numpy as np

with open("Day09/input_AJRF.txt") as f:
    input = f.readlines()

input_mat = np.array([list(line.strip()) for line in input], dtype = "int")
(row, col) = input_mat.shape

## Add 9s around the edge
new_mat = np.ones((row+2, col+2)) * 9
new_mat[1:-1, 1:-1] = input_mat
new_mat

low_points = [item for i, row in enumerate(input_mat) for j, item in enumerate(row) \
    if item < new_mat[i + 1][j]
    and item < new_mat[i + 1][j + 2]
    and item < new_mat[i][j + 1]
    and item < new_mat[i + 2][j + 1]]

risk = sum(low_points) + len(low_points) # add 1 for each point
print("Risk score:", risk)

# Part 2
# init an array for basin sizes
basins = np.zeros(len(low_points))
input_mat_2 = input_mat.copy()
for basin_i, basin in enumerate(basins):
    done = False
    started = False
    basin_value = 10 + basin_i

    # loop multiple times til that basin is complete
    still_adding = True
    while still_adding:
        still_adding = False
        for i, row in enumerate(input_mat_2):
            for j, item in enumerate(row):
                if item < 9:
                    if not(started):
                        started = True
                        basins[basin_i] += 1
                        input_mat_2[i][j] = basin_value
                        still_adding = True
                    # else if above, below, left or right is basin_value this also be part of basin 
                    # though need to do this multiple times as left and below won't exist first time round
                    elif ((i > 0) and (input_mat_2[i-1][j] == basin_value)) | \
                        ((i < (len(input_mat_2)-1)) and (input_mat_2[i+1][j] == basin_value)) | \
                        ((j > 0) and (input_mat_2[i][j-1] == basin_value)) | \
                        ((j < (len(row)-1)) and (input_mat_2[i][j+1] == basin_value)):
                        
                        basins[basin_i] += 1
                        input_mat_2[i][j] = basin_value
                        still_adding = True

#basins

## three largest basins, multiplied
answer = np.product(np.sort(basins)[-3:])
print("Largest three basin sizes multiply to", answer)


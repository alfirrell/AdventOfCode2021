#%% set up data
import numpy as np

with open("Day11/input_AJRF.txt") as f:
    input = f.readlines()

input_array = np.array([list(line.strip()) for line in input], dtype = "int")
input_array

#%% increment steps

def increment_adjacent(row, col):
    now_over_nine = []
    for r in np.arange(row - 1, row + 2):
        # print(r)
        for c in np.arange(col - 1, col + 2):
            # print(c)
            if not(r == row and c == col) and \
                r >= 0 and r <= 9 and \
                c >= 0 and c <= 9:
                # print(r, c)
                if (new_input[r, c] == 9):
                    now_over_nine.append((r, c))
                new_input[r, c] += 1
    return(now_over_nine)

def keep_incrementing(over_nine):
    for (r, c) in over_nine:
        adj_over_nine = increment_adjacent(r, c)
        if len(adj_over_nine) > 0:
            zeroise.extend(adj_over_nine)
            keep_incrementing(adj_over_nine)

new_input = input_array
flash_count = 0
# Step: add 1, identify any > 9, add one to each one around them and set them to zero, repeat until no more over 9
for step in np.arange(100):

    ## add 1 to everything
    new_input = new_input + 1
    
    zeroise = []
    # find those over 9 
    over_nine = new_input > 9
    if (np.count_nonzero(over_nine) > 0):
        ## flash the over-9s 
        rows, cols = np.where(over_nine)
        rc_pairs = list(zip(rows, cols))
        zeroise.extend(rc_pairs)
        for rc_pair in rc_pairs:
            keep_incrementing([rc_pair])
    
        for (row, col) in zeroise:
            new_input[row, col] = 0
            flash_count += 1

print("Flash count = ", flash_count)

# %% Part 2
# Repeat the loop until everything goes to zero
new_input = input_array
all_flash = False
step_count = 0

while not(all_flash):
    step_count += 1
    ## add 1 to everything
    new_input = new_input + 1
    
    zeroise = []
    # find those over 9 
    over_nine = new_input > 9
    if (np.count_nonzero(over_nine) > 0):
        ## flash the over-9s 
        rows, cols = np.where(over_nine)
        rc_pairs = list(zip(rows, cols))
        zeroise.extend(rc_pairs)
        for rc_pair in rc_pairs:
            keep_incrementing([rc_pair])
    
        for (row, col) in zeroise:
            new_input[row, col] = 0
        
        all_flash = np.all(new_input == 0)

print("All flash at step #", step_count)
# %%


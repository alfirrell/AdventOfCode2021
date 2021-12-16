import numpy as np

with open("Day13/input_AJRF.txt", "r") as f:
    input = f.readlines()

dots = []
folds = []

for line in input:
    line = line.strip()
    if line == "":
        continue
    elif line.startswith("fold"):
        axis, value = line.replace("fold along ", "").split("=", 2)
        folds.append((axis, int(value)))
    else:
        col, row = line.strip().split(",", 2)
        dots.append((int(row), int(col)))

max_row, max_col = np.max(np.array(dots), axis = 0)

grid = np.zeros([max_row + 1, max_col + 1])
for (row, col) in dots:
    grid[row,col] = 1

#grid

def fold(grid, fold_axis, fold_value):
        
    # Do the fold
    if fold_axis == 'x':
        orig_part = grid[:, :fold_value]
        flip_part = np.fliplr(grid[:, (fold_value + 1):]) # flip left-right
    else:
        orig_part = grid[:fold_value, :]
        flip_part = np.flipud(grid[(fold_value + 1):, :]) # flip up-down

    # ## Make both parts the bigger size: NOT REQUIRED
    # max_shape = max(orig_part.shape, flip_part.shape)
    # orig_part_new = flip_part_new = np.zeros(max_shape)
    # orig_part_new[max_shape[0] - orig_part.shape[0]:, max_shape[1] - orig_part.shape[1]:] = orig_part
    # flip_part_new[max_shape[0] - flip_part.shape[0]:, max_shape[1] - flip_part.shape[1]:] = flip_part

    overlap = (orig_part > 0) | (flip_part > 0)
    overlap = 1*overlap
    return(overlap)

fold_axis, fold_value = folds[0]
new_grid = fold(grid, fold_axis, fold_value)

print("Number of dots:", np.sum(overlap))

# Part 2
new_grid = grid
for (fold_axis, fold_value) in folds:
    new_grid = fold(new_grid, fold_axis, fold_value)

## View the final code: 8 characters
print_lines = [''.join(['\u2588' if col == 1 else ' ' for col in line]) for line in new_grid]
for pl in print_lines:
    print(pl)




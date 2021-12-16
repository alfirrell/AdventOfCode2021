import numpy as np
import pandas as pd

points = pd.read_csv("Day05/input_AJRF.txt", \
        sep=",| -> ", header=None, \
        names=["from_x", "from_y", "to_x", "to_y"], \
        engine="python")

# Horizontal and vertical only
points["is_horiz"] = points["from_y"] == points["to_y"]
points["is_vert"] = points["from_x"] == points["to_x"]

horiz_vert = points[points["is_horiz"] | points["is_vert"]]

def gen_line_points(row):
    h_step = 1 if row["from_x"] <= row["to_x"] else -1
    v_step = 1 if row["from_y"] <= row["to_y"] else -1
    h_range = np.arange(row["from_x"], row["to_x"] + h_step, h_step)
    v_range = np.arange(row["from_y"], row["to_y"] + v_step, v_step)
    if len(h_range) == 1:
        h_range = np.repeat(h_range, len(v_range))
    if len(v_range) == 1:
        v_range = np.repeat(v_range, len(h_range))
    df = pd.DataFrame({"x": h_range, "y": v_range})

    return(df)

line_points = horiz_vert.apply(gen_line_points, axis = 1)
line_points = pd.concat(line_points.to_list(), ignore_index=True)

counts = line_points.value_counts()
len(counts[counts>=2])

## Part 2: adding the diagonals (45 deg)

# Improved function: this works for horiz, vert and diag without needing to check
def gen_line_points2(row):

    h_step = 1 if row["from_x"] <= row["to_x"] else -1
    v_step = 1 if row["from_y"] <= row["to_y"] else -1
    h_range = np.arange(row["from_x"], row["to_x"] + h_step, h_step)
    v_range = np.arange(row["from_y"], row["to_y"] + v_step, v_step)
    if len(h_range) == 1:
        h_range = np.repeat(h_range, len(v_range))
    if len(v_range) == 1:
        v_range = np.repeat(v_range, len(h_range))
    df = pd.DataFrame({"x": h_range, "y": v_range})

    return(df)

## all points - incl diags
line_points = points.apply(gen_line_points2, axis = 1)
line_points = pd.concat(line_points.to_list(), ignore_index=True)

counts = line_points.value_counts()
len(counts[counts>=2])


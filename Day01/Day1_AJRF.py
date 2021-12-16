import pandas as pd

# Part 1: compare reading to previous and count increases
df = pd.read_csv("Day01/input.txt", header=None, names = ["reading"])
df["previous"] = df["reading"].shift()
df["increased"] = df["reading"] > df["previous"]
# Count increases
df["increased"].sum()

# Part 2: windowed sum of 3
df["window_sum"] = df["reading"] + df["reading"].shift(-1) + df["reading"].shift(-2) # could also do with rolling sum
df["window_sum_increased"] = df["window_sum"] > df["window_sum"].shift()
# Count increases
df["window_sum_increased"].sum()

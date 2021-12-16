import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv("Day03/input.txt", header=None, names = ["code"], dtype={"code":"string" })

code_length = len(df["code"][0])

gamma = ''
epsilon = ''

for position in range(code_length):
    position_sum = sum([int(code[position]) for code in df["code"]])

    ## If sum > half of number of rows, is mostly '1'
    mostly_1 = position_sum >= (len(df) / 2)
    gamma += '1' if mostly_1 else '0'
    epsilon += '0' if mostly_1 else '1'

gamma_int = int(gamma, 2)
epsilon_int = int(epsilon, 2)
print(gamma_int, epsilon_int, gamma_int * epsilon_int)

## Part 2
# Oxygen: find most common, CO2 find least common in each position
# Scan through twice because I'm lazy
df_subset = df.copy()
for position in range(code_length):
    df_subset.loc[:, "active_code"] = [int(code[position]) for code in df_subset["code"]]
    most_frequent = 1 if sum(df_subset["active_code"]) >= (len(df_subset) / 2) else 0
    df_subset = df_subset[df_subset["active_code"] == most_frequent].copy()
    # break if there's only one row left
    if (len(df_subset) == 1):
        oxygen_rating = df_subset["code"].iloc[0]
        break

df_subset = df.copy()
for position in range(code_length):
    df_subset.loc[:, "active_code"] = [int(code[position]) for code in df_subset["code"]]
    least_frequent = 0 if sum(df_subset["active_code"]) >= (len(df_subset) / 2) else 1
    df_subset = df_subset[df_subset["active_code"] == least_frequent].copy()
    # break if there's only one row left
    if (len(df_subset) == 1):
        co2_rating = df_subset["code"].iloc[0]
        break

o2_int = int(oxygen_rating, 2)
co2_int = int(co2_rating, 2)
life_support_rating = o2_int * co2_int
print(o2_int, co2_int, life_support_rating)

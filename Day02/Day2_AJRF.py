import pandas as pd
import numpy as np

df = pd.read_csv("Day02/input.txt", sep = " ", header=None, names = ["direction", "value"])
df["signed_value"] = np.where(df["direction"]=="up", df["value"] * -1, df["value"])

df["forward"] = np.where(df["direction"] == "forward", df["signed_value"] , 0)
df["up_down"] = np.where(df["direction"] != "forward", df["signed_value"] , 0)

horizontal = df["forward"].sum()
vertical = df["up_down"].sum()
horizontal * vertical

## Part 2
df["aim"] = df["up_down"].cumsum()
df["depth_change"] = df["forward"] * df["aim"]
df["depth"] = df["depth_change"].cumsum()

df["depth"].iloc[-1] * horizontal
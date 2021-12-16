import numpy as np
import pandas as pd

#%% Load data
#input_txt = "3,4,3,1,2"
with open("input_AJRF.txt") as f:
    input_txt = f.readline()

inputs = input_txt.split(",")
inputs = np.array(inputs, dtype = "int")

#%% Part 1
inputs_new = inputs
for day in range(80):
    inputs_new = inputs_new - 1
    spawns = np.where(inputs_new == -1)[0]
    n_spawns = len(spawns)
    if n_spawns > 0:
        inputs_new[spawns] = 6
        inputs_new = np.append(inputs_new, np.repeat(8, n_spawns))

    #print(inputs)

len(inputs_new)

#%% But this gets slow quite quickly: speed test
import time

time_list = []
for num_days in np.arange(10, 161, 10):
    start = time.time()
    inputs_new = inputs
    for day in range(num_days):
        inputs_new = inputs_new - 1
        spawns = np.where(inputs_new == -1)[0]
        n_spawns = len(spawns)
        if n_spawns > 0:
            inputs_new[spawns] = 6
            inputs_new = np.append(inputs_new, np.repeat(8, n_spawns))

        #print(inputs)

    #len(inputs_new)
    elapsed = time.time() - start
    print(num_days, "days,", len(inputs_new), "fish, time:", round(elapsed, 1)
    time_list.append([num_days, elapsed])

from matplotlib import pyplot as plt

times_df = pd.DataFrame(time_list)
plt.plot(times_df[0], times_df[1])
plt.show()


#%% Part 2

## NEED A NEW APPROACH!
num_ages = 9
num_fish_at_age = np.zeros(num_ages)  ## empty counts

# Count num at each age
unique, counts = np.unique(inputs, return_counts=True)
counts_dict = dict(zip(unique, counts))
# ... and put into the vector (in case there are some missing ages)
for age, count in counts_dict.items():
    num_fish_at_age[age] = count

# Func to move counts to the next period
def next_period(fish_counts):
    new_fish_counts = np.zeros(num_ages)
    # for fish at day 1-8, move them one day lower (0-7)
    new_fish_counts[:-1] = fish_counts[1:]

    # for each fish currently at day zero, 
    #  restart them at 6, and spawn a new one at 8
    new_fish_counts[6] += fish_counts[0]
    new_fish_counts[8] += fish_counts[0]

    return(new_fish_counts)

# Iterate through periods updating the count
for i in range(256):
    num_fish_at_age = next_period(num_fish_at_age)
    #print(np.sum(num_fish_at_age))

print(np.sum(num_fish_at_age))


from collections import Counter

with open("Day14/input_AJRF.txt", "r") as f:
    input = f.readlines()

input_clean = input[0].strip()
inserts = [line.strip().split(" -> ") for line in input[2:]]
replacements = {from_str: from_str[0] + insert + from_str[1] for from_str, insert in inserts}

def replace_pairs(pair_string):
    pairs = [pair_string[i:i+2] for i in range(len(pair_string) - 1)]

    updated_pairs = [replacements[pair] if pair in replacements.keys() else pair for pair in pairs]
    updated_pairs_without_overlap = [pair[:-1] if i < (len(updated_pairs)-1) else pair for i, pair in enumerate(updated_pairs)]
    
    rejoined = ''.join(updated_pairs_without_overlap)
    return(rejoined)

new_string = input_clean
for i in range(10):
    new_string = replace_pairs(new_string)

letter_counts = Counter(new_string)
ordered_counts = letter_counts.most_common()
print("Most common minus least common =", ordered_counts[0][1] - ordered_counts[-1][1])

## Part 2 - do 40 loops
## BUT... it's going exponential again... so can we just do counts, not construct the string?

# So each pair turns into two pairs
# e.g. CH -> B means CH becomes CB, HB
# create a matrix with these and mark the transitions
# then we can repeated apply this and count up each pair
import numpy as np

pairs = np.array(inserts)[:,0] # NB have checked all the pair combinations exist already
num_pairs = len(pairs)
transition = np.zeros((num_pairs, num_pairs))
for pair, insert in inserts:
    new_pair_1 = pair[0] + insert
    new_pair_2 = insert + pair[1]
    #print(pair, "->", (new_pair_1, new_pair_2))
    pair_idx = np.where(pairs == pair)[0][0]
    new_pair_1_idx = np.where(pairs == new_pair_1)[0][0]
    new_pair_2_idx = np.where(pairs == new_pair_2)[0][0]
    #print(pair_idx, "->", new_pair_1_idx, new_pair_2_idx)
    transition[new_pair_1_idx, pair_idx] = 1
    transition[new_pair_2_idx, pair_idx] = 1

transition

start_pairs = [input_clean[i:i+2] for i in range(len(input_clean) - 1)]
start_array = np.zeros(num_pairs)
for pair in start_pairs:
    pair_idx = np.where(pairs == pair)[0][0]
    start_array[pair_idx] += 1
start_array

arr = start_array
for i in range(40):
    arr = np.sum(arr * transition, axis=1)

letters = list(set(list(zip(*inserts))[1]))

## Count up.  As we have overlapping pairs, will be doubled for all but the first and last letter
## So artifically add one for these, and then half everything
letter_counts = dict(zip(letters, np.zeros(len(letters))))
letter_counts[input_clean[1]] += 1
letter_counts[input_clean[-1]] += 1

for i, pair in enumerate(pairs):
    letter_counts[pair[0]] += arr[i]
    letter_counts[pair[1]] += arr[i]

letter_counts = {k: int(v/2) for k,v in letter_counts.items()}

ordered_counts = Counter(letter_counts).most_common()
print("Most common minus least common =", ordered_counts[0][1] - ordered_counts[-1][1])

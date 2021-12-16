import re
import statistics as stats

with open("Day10/input_AJRF.txt") as f:
    input = f.readlines()

input = [line.strip() for line in input]
#input

points = {')':3, ']':57, '}':1197, '>': 25137}

total_points = 0
valid = []
# iterate through removing adjacent open-close pairs
# (effectively working from the middle out)
# once we've remove all these, anything left is 
# (i) hanging openers (incomplete), and
# (ii) hanging closers (errors)
for line in input:

    done = False
    while not(done):
        line_len = len(line)
        for replace_me in ["()", "[]", "{}", "<>"]:
            line = line.replace(replace_me, "")

        if line_len == len(line):
            done = True

    line
    # look for closers
    closers_pattern = "[\\]\\)\\>\\}]"
    search = re.search(closers_pattern, line)
    if not(search == None):
        error_char = search.group()
        error_char_points = points[error_char]
        total_points += error_char_points
    else:
        valid.append(line)

total_points
valid

# Part 2
## valid list added above to capture the incomplete ones
# work from right to left calculating score
scores = {"(": 1, "[": 2, "{": 3, "<": 4 }
total_scores = []
for valid_line in valid:
    total = 0
    for char in valid_line[::-1]:
        total = total * 5 + scores[char]

    total_scores.append(total)

print("Middle score is", stats.median(total_scores))
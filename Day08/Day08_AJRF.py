import numpy as np
import pandas as pd

# Part 1
readings = pd.read_csv("Day08/input.txt", sep = "|", header=None, names=["digits","output"])

## Count digits of length 2 (1), 3 (7), 4 (4), 7 (8)
num_digits = [len(digit) in [2,3,4,7] for output in readings["output"] for digit in output.strip().split(" ", 4)]
sum(num_digits)

# Part 2 - work 'em all out!

def sort_str(x):
    return("".join(sorted(x)))

# This feels long-winded, but is at least simple...
def get_output_value(reading):
    
    digits = reading["digits"].strip().split(" ")
    digits = [sort_str(digit) for digit in digits] ## sort for consistency of lookups later
    digits = np.array(digits)

    lengths = np.array(list(map(len, digits)))

    mapping = dict()
    # 1, 7, 4 and 8 have unique lengths (2,3,4,7) so get them out first
    mapping["1"] = digits[lengths == 2][0]
    mapping["7"] = digits[lengths == 3][0]
    mapping["4"] = digits[lengths == 4][0]
    mapping["8"] = digits[lengths == 7][0]

    # length 6 digits are 0, 6 and 9. 
    all_segments = set(mapping["8"])
    six_seg_digits = digits[lengths == 6] 
    missing_seg = [element for digit in six_seg_digits for (element, ) in all_segments.difference(set(digit))]
    # The missing item from the 6 is in the 1
    six_idx = [i for (i, seg) in enumerate(missing_seg) if seg in mapping["1"]][0]
    # The missing item from the 0 is in the 4, not the 1
    zero_idx = [i for (i, seg) in enumerate(missing_seg) if seg in mapping["4"] and not(seg in mapping["1"])][0]
    # so the nine is the other one
    nine_idx = [i for i,x in enumerate(six_seg_digits) if not(i in [six_idx, zero_idx])][0]
    mapping["6"] = six_seg_digits[six_idx]
    mapping["0"] = six_seg_digits[zero_idx]
    mapping["9"] = six_seg_digits[nine_idx]

    # ...leaving 2, 3 and 5 which are five-segment digits.
    five_seg_digits = digits[lengths == 5]
    # 3 has both elements of 1
    three_idx = [i for i, digit in enumerate(five_seg_digits) if len(set(mapping["1"]).difference(set(digit))) == 0][0]
    # 2 contains the segment 9 is missing
    nine_missing_seg = missing_seg[nine_idx]
    two_idx = [i for i, digit in enumerate(five_seg_digits) if nine_missing_seg in digit][0]
    # and five is the last one
    five_idx = [i for i,x in enumerate(five_seg_digits) if not(i in [three_idx, two_idx])][0]
    mapping["3"] = five_seg_digits[three_idx]
    mapping["2"] = five_seg_digits[two_idx]
    mapping["5"] = five_seg_digits[five_idx]

    # Flip the dict for output lookup
    output_mapping = dict(zip(mapping.values(), [int(key) for key in mapping.keys()]))
    # Lookup the integer from the dict for each output string
    output_digits = [str(output_mapping[sort_str(digit)]) for digit in reading["output"].strip().split(" ")]
    # and turn into a 4 digit int
    output_value = int("".join(output_digits))
    return(output_value)

output_values = readings.apply(get_output_value, axis = 1)
print(sum(output_values))
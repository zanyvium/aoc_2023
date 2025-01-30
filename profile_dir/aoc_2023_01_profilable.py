import numpy as np
from utils.utils_puzzle_2023_01 import word_to_num_map
# Solution 1: Crude for loops:

def aoc_2023_01_sol_1_func(puzzle_input):
    #### Implementation Step 1
    num_list_raw = []

    #### Implementation Step 2
    for line in puzzle_input.split("\n"):
        numbers_in_line = ""
        line_mod = line
        for key, value in word_to_num_map.items():
            #!!! assume text digits do not overlap (eg. no 'twone')
            line_mod = line_mod.replace(key, value) 
        for ch in line_mod:
            if ch.isdigit():
                numbers_in_line += ch
        num_list_raw.append(numbers_in_line)

    #### Implementation Step 3
    num_list_mod = []
    for nums_in_line in num_list_raw:
        if len(num_list_raw) == 0:
            num_list_mod.append(0)
        elif len(num_list_raw) == 1:
            #!!! >=1 could be collected into a single line with [0] + [-1]
            nums_in_line.append(nums_in_line[0] + nums_in_line[0]) 
        else:
            num_list_mod.append(nums_in_line[0] + nums_in_line[-1])

    first_last_num = []
    for fr in num_list_mod:
        first_last_num.append(int(fr))
    first_last_num = np.array(first_last_num)

    #### Implementation Step 4
    return np.sum(first_last_num)
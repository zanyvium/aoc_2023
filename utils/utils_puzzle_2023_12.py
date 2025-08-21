import numpy as np

import itertools
from typing import Callable, Iterator

# # Let's make a function for trimming the beginning and end of lines for "."s
# we use "in {}" speedup as benchmarked to be faster than "== or ==" or "in []"
# !!! 25-06-08: Should be able to speed up more by having indices not materialised 
# !!! 25-06-08: Not actually used in solution 1
def trim_ccr(s: str):
    question_pound_indices = [i for i, char in enumerate(s) if char in {"?", "#"}]
    line_trimmed = s[question_pound_indices[0]:(question_pound_indices[-1]+1)]
    
    return line_trimmed if question_pound_indices else s

def reformat_pis(puzzle_input_split: list[str]):
    pis_ccr, pis_wsr = map(list, zip(*[line.split(" ") for line in puzzle_input_split]))

    pis_ccr = list(map(trim_ccr, pis_ccr)) # not strictly neccessary for solutions implmented here
    pis_wsr = [[int(num) for num in check.split(",")] for check in pis_wsr]

    return pis_ccr, pis_wsr

# Generate PCRs
def generate_pcr(n: int, combinants: list[str], condition: Callable[[str], bool] = lambda st: True) -> Iterator[str]:
    return (
        ''.join(p) for p in itertools.product(combinants, repeat=n)
        if condition(''.join(p))
    )

# KCR filter function:
def filter_pcr_by_kcr(pcr: str, kcr_filter: dict[int, str]) -> bool:
    return True if all(pcr[i] == kcr_filter[i] for i in kcr_filter) else False


# Let's create a function that generates the kcr filter dictionaries:
def generate_kcr_filter_from_ccr(ccr: str, known_components: set[str] = {".", "#"}) -> dict[int, str]:
    return {i: char for i, char in enumerate(ccr) if char in known_components}

# Let's create a closure function
def generate_kcr_filter_func_from_ccr(ccr: str, known_components: set[str] = {".", "#"}) -> Callable[[str], bool]:
    kcr_filter = generate_kcr_filter_from_ccr(ccr = ccr, known_components=known_components)
    def filter_pcr(pcr: str) -> bool:
        return filter_pcr_by_kcr(pcr = pcr, kcr_filter=kcr_filter)
    return filter_pcr

def generate_psr_from_pcr(pcr: str) -> list[int]:
    return [len(component) for component in pcr.split(".") if component]


def calc_num_pcr_from_ccr(ccr: str, wsr: list[int]) -> int:
    filter_func = generate_kcr_filter_func_from_ccr(ccr = ccr)
    len_ccr = len(ccr)
    desired_combinants = ["#", "."]
    return sum(
        1
        for pcr in generate_pcr(n = len_ccr, combinants = desired_combinants, condition = filter_func)
        if generate_psr_from_pcr(pcr = pcr) == wsr
    )


def show_num_pcr_from_ccr(ccr: str, wsr: list[int]) -> None:
    i = 0
    filter_func = generate_kcr_filter_func_from_ccr(ccr = ccr)
    print(f"ccr: {ccr}, wsr: {wsr}\n")
    for pcr in generate_pcr(len(ccr), ["#", "."], filter_func):
        psr = generate_psr_from_pcr(pcr)
        if psr == wsr:
            print(f"pcr: {pcr}, psr: {psr}")
            i += 1
    print(f"\ntotal number of pcrs: {i}\n")



def solve_puzzle(puzzle_input_split):
    pis_ccr, pis_wsr = reformat_pis(puzzle_input_split)

    nums = [calc_num_pcr_from_ccr(ccr, wsr) for ccr, wsr in zip(pis_ccr, pis_wsr)]
    return sum(nums)


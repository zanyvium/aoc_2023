import os
import numpy as np
import requests
import pickle
from utils.cookie_val import cookie_val

def _generate_input_pickle_name(year, day):
    if day < 10:
        return f"puzzle_input_{year}_0{day}.pkl"
    else: 
        return f"puzzle_input_{year}_{day}.pkl"

def _fetch_input(year, day, session_cookie = cookie_val):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {
        "Cookie": f"session={session_cookie}",
        "User-Agent": "https://github.com/zanyvium/aoc_2023 by vzn",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text.strip()  # Remove any leading/trailing whitespace
    else:
        raise Exception(f"Failed to fetch input: {response.status_code}, {response.reason}")

def _save_input(*, response, pickle_name, save_path= "./data/"):
    with open(save_path + pickle_name, "wb") as file:
        pickle.dump(response, file)

def load_input(year, day, session_cookie = cookie_val, save_path = "./data/"):
    assumed_pickle_name = _generate_input_pickle_name(year = year, day = day)
    path_and_name = save_path + assumed_pickle_name

    puzzle_input = None

    if os.path.exists(path_and_name):
        with open(path_and_name, "rb") as file:
            puzzle_input = pickle.load(file)
            print("loaded puzzle input")
    else:
        puzzle_input = _fetch_input(year = year, day = day, session_cookie = session_cookie)
        _save_input(response = puzzle_input, pickle_name = assumed_pickle_name, save_path = save_path)
        print(f"saved puzzle input {save_path + assumed_pickle_name}")

    return puzzle_input
    
def split_puzzle_input(puzzle_input) -> list:
    return list(puzzle_input.split("\n"))

def matrix_puzzle_input(puzzle_input) -> np.ndarray:
    puzzle_input_split = split_puzzle_input(puzzle_input)
    return np.array(list(map(lambda x: list(x), puzzle_input_split)))
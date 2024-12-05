from dotenv import dotenv_values
from pathlib import Path
import requests
import time
import json
import re

THIS_DIR = Path(__file__).parent
SOLVED_FILE = THIS_DIR / "./solved.json"
dotenv = dotenv_values(THIS_DIR / ".env")


def read_input_day(day):
    # Check if input is cached
    input_cache_file = THIS_DIR / f"./inputs/day_{day}.txt"
    if input_cache_file.exists():
        with open(input_cache_file, "r") as fd:
            return fd.read()
    # Otherwise, fetch input from AoC
    req = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies={ "session": dotenv["AOC_SESSION_COOKIE"] })
    input_text = re.sub(r"[\t ]+", " ", req.text.strip())
    # Cache input
    with open(input_cache_file, "w") as fd:
        fd.write(input_text)
    return input_text

def time_solve(func):
    import timeit
    print("Timing solve function.... (100 runs)")
    res = timeit.timeit(func, number=100) * 10
    print(str(round(res, 2)) + " ms per solve")

def submit_result_day(day, part, answer, allow_zero=False, allow_negative=False):
    # If the answer is a function. Time it first
    if callable(answer):
        time_solve(answer)
        answer = answer()

    # Check if answer is valid before submitting
    if not str(answer).isnumeric():
        print(f"Answer for day {day}, part {part} is not numeric, skipping submission")
        return
    if not allow_zero and int(answer) == 0:
        print(f"Answer for day {day}, part {part} is 0, skipping submission")
        return
    if not allow_negative and int(answer) < 0:
        print(f"Answer for day {day}, part {part} is negative, skipping submission")
        return
    print(f"Submitting answer day {day}, part {part}: {answer}")

    # Check if already solved
    solved_key = f"day_{day}_part_{part}"
    with open(SOLVED_FILE, "r") as fd:
        solved = json.load(fd)
    if solved_key in solved:
        print("Already solved, skipping submission")
        return

    # Submit answer to AoC
    req = requests.post(f"https://adventofcode.com/2024/day/{day}/answer", cookies={ "session": dotenv["AOC_SESSION_COOKIE"] }, data={ "level": part, "answer": answer })
    response = req.text
    if "That's the right answer!" in response:
        print("Success!")
        solved[solved_key] = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "answer": answer
        }
        with open(SOLVED_FILE, "w") as fd:
            fd.write(json.dumps(solved, indent=4))
    elif "That's not the right answer" in response:
        print("Failed: Wrong answer")
    elif "Did you already complete it?" in response:
        print("Failed: Puzzle already completed")
    else:
        print("Failed: Unknown error")
        print(response)
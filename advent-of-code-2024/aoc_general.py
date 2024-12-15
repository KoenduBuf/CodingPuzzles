from dotenv import dotenv_values
from pathlib import Path
import requests
import time
import json
import sys
import re

THIS_DIR = Path(__file__).parent
SOLVED_FILE = THIS_DIR / "./solved.json"
dotenv = dotenv_values(THIS_DIR / ".env")

sys.path.append(str(THIS_DIR.parent))


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
    input_cache_file.parent.mkdir(exist_ok=True)
    with open(input_cache_file, "w") as fd:
        fd.write(input_text)
    return input_text

def time_solve(func):
    import timeit
    print("Timing solve function....")
    single_time = timeit.timeit(func, number=1)
    do_runs = int(10 // single_time)
    if do_runs > 0:
        single_time = timeit.timeit(func, number=do_runs) / do_runs
    print(f"{round(single_time * 1000, 2)} ms per solve ({max(do_runs, 1)} runs)")

def submit_result_day(day, part, answer, allow_zero=False, allow_negative=False, time_solve=False):
    if time_solve and callable(answer):
        time_solve(answer)

    answer = answer() if callable(answer) else answer

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
        print("Already solved, skipping submission.")
        print("Answer was " + ("correct" if solved[solved_key]["answer"] == answer else "incorrect"))
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
    elif "You gave an answer too recently" in response:
        print("Failed: Answered too recently")
    else:
        print("Failed: Unknown error")
        print(response)
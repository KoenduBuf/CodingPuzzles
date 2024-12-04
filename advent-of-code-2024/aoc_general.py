from dotenv import dotenv_values
from pathlib import Path
import requests
import re

THIS_DIR = Path(__file__).parent
dotenv = dotenv_values("./.env")


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


def submit_result_day(day, part, result, allow_zero=False, allow_negative=False):
    if not str(result).isnumeric():
        print(f"Result for day {day}, part {part} is not numeric, skipping submission")
        return
    if not allow_zero and int(result) == 0:
        print(f"Result for day {day}, part {part} is 0, skipping submission")
        return
    if not allow_negative and int(result) < 0:
        print(f"Result for day {day}, part {part} is negative, skipping submission")
        return
    print(f"Submitting result day {day}, part {part}: {result}")
    # Submit result to AoC
    req = requests.post(f"https://adventofcode.com/2024/day/{day}/answer", cookies={ "session": dotenv["AOC_SESSION_COOKIE"] }, data={ "level": part, "answer": result })
    response = req.text
    if "That's the right answer!" in response:
        print("Success!")
    elif "That's not the right answer" in response:
        print("Failed: Wrong answer")
    elif "Did you already complete it?" in response:
        print("Failed: Puzzle already completed")
    else:
        print("Failed: Unknown error")
        print(response)
#!/usr/bin/env python3

import subprocess
import random
import time
import sys
import os

def runprint(*args, **kwargs):
    print("\033[94m", end="")
    print(" ".join(map(str,args)), **kwargs)
    print("\033[0m")


def calc_bulls_and_cows(actualNumber, guessedNumber):
    bulls = len( list(filter(lambda t: t[0] == t[1], zip(actualNumber, guessedNumber))) )
    in_actual_number = list(actualNumber)
    is_in_and_remove = lambda d: d in in_actual_number and in_actual_number.remove(d) == None
    cows = len( list(filter(is_in_and_remove, guessedNumber)) ) - bulls
    return (bulls, cows)


def create_number(num_input, unique):
    if num_input > 10: return str(num_input)
    number = ""
    for l in range(num_input):
        while True:
            i = random.randint(0 if l > 0 else 1, 9)
            if unique and str(i) in number: continue
            number += str(i)
            break
    return number


def do_turn(proc, num_len, number, debug=False):
    guess = proc.stdout.readline().strip()
    if proc.poll() is not None:
        runprint(f"FAIL! - Exe exit: {proc.poll()}")
        return "fail"

    if len(guess) == 0:
        runprint(f"FAIL! Weird empty output thing...")
        return "fail" # Happens when we crashed it seems

    if debug: runprint(f"\nExecutable guessed '{guess}'")
    if guess[0] == '0' or len(guess) != num_len:
        runprint(f"FAIL! - Invalid guess: {guess}")
        return "fail"

    if len(set(guess)) != len(guess):
        runprint(f"FAIL! - Digits not unique: {guess}")
        return "fail"

    bulls, cows = calc_bulls_and_cows(number, guess)
    if bulls == num_len:
        if debug: runprint("SUCCESS!")
        return "win"

    proc.stdin.write(f"{bulls} {cows}\n")
    proc.stdin.flush()


def run_exe(exe, num_input, debug=False):
    number = create_number(num_input, True)
    num_len = len(number)
    start_time = int(time.time() * 1000)
    max_turn_time = 0
    runprint(f"Random number (len {len(number)}) is {number} -> ", end="\n" if debug else "")
    with subprocess.Popen(f"./{exe}", shell=False, encoding="UTF-8",
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=None if debug else subprocess.DEVNULL) as proc:

        proc.stdin.write(f"{num_len}\n")
        proc.stdin.write(f"0 0\n")
        proc.stdin.flush()

        turn = 0
        while True:
            turn_start = time.time() * 1000
            r = do_turn(proc, num_len, number, debug)
            turn_time = int(time.time() * 1000 - turn_start)
            max_turn_time = max(turn_time, max_turn_time)
            turn += 1
            if r is not None: break     # we got win or fail
            if (turn <= 50): continue
            runprint("FAIL! - Too many turns!")
            break
    total_time = int(time.time() * 1000) - start_time
    if r == "win":
        runprint(f"Executable won in {turn} turns")
        return turn, total_time, max_turn_time
    return 301, total_time, max_turn_time


def run_bunch(exe, num_len, runs, debug=False):
    total_turns, total_time, max_time, fails = 0, 0, 0, 0
    for _ in range(runs):
        trun, timet, timem = run_exe(exe, num_len, debug)
        max_time = max(timem, max_time)
        if trun > 300: fails += 1
        total_time += timet
        total_turns += trun
    avg_turns = round(total_turns / runs, 2)
    avg_time_per_turn = round(total_time/total_turns, 1)
    print(f"Num len {str(num_len).rjust(2)} - {runs-fails}/{runs} runs: ", end="")
    print(f"{str(avg_turns).rjust(5)} turns, {str(avg_time_per_turn).rjust(4)} ms/turn avg, max: {str(int(max_time)).rjust(4)} ms")
    return (total_time, total_turns, fails, avg_turns, avg_time_per_turn)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Use as: {sys.argv[0]} <executable (or .c)> <num-(len)> [times]")
        sys.exit(1)

    debug = "-d" in sys.argv
    if debug: sys.argv.remove("-d")
    exe = sys.argv[1]

    remove_files = [ ]
    compile = {
        'c':    "gcc {} -Wall -o {}",
        'cpp':  "g++ {} -Wall -o {}"
    }
    extension = exe.rsplit('.', 1)[-1]
    if extension in compile:
        nexe = "./" + exe[:-len(extension)][:-1]
        os.system(compile[extension].format(exe, nexe))
        if not os.path.isfile(exe):
            print("Failed to create runnable")
            exit(1)
        exe = nexe
        remove_files.append(exe)

    # Run the actual thing

    num_lenl = list(range(1, 11)) if sys.argv[2] == 'all' else [int(sys.argv[2])]
    if len(num_lenl) > 1: runprint = lambda s, *args, **kwargs: 0
    runs = int(sys.argv[3]) if len(sys.argv) >= 4 else 1
    for num_len in num_lenl:
        run_bunch(exe, num_len, runs, debug)

    # Remove created files

    for f in remove_files:
        os.system(f"rm ./{f}")

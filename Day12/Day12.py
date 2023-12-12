""" Advent of Code 2023, Day 12
    Day 12: Hot Springs
    Author: Chi-Kit Pao
"""

import itertools
import os
import time


def parse_line(line):
    pattern, p2 = line.split()
    number_values = eval(f"({p2})")
    return pattern, number_values


def test_pattern(pattern, number_values):
    pattern_list = list(pattern)
    question_mark_positions = [
        i for i in range(len(pattern_list)) if pattern_list[i] == "?"
    ]
    result = 0
    for p in itertools.product((".", "#"), repeat=len(question_mark_positions)):
        for i, pos in enumerate(question_mark_positions):
            pattern_list[pos] = p[i]
        damage_count = tuple(
            [len(list(g)) for k, g in itertools.groupby(pattern_list) if k == "#"]
        )
        if damage_count == number_values:
            result += 1
    return result


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    result1 = 0
    for line in lines:
        pattern, number_values = parse_line(line)
        result1 += test_pattern(pattern, number_values)

    print(
        "Question 1: For each row, count all of the different arrangements of\n"
        " operational and broken springs that meet the given criteria. What\n"
        " is the sum of those counts?"
    )
    print(f"Answer: {result1}")
    #print(
    #    "Question 2: Unfold your condition records; what is the new sum of\n"
    #    " possible arrangement counts?"
    #)
    #print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: For each row, count all of the different arrangements of
#  operational and broken springs that meet the given criteria. What
#  is the sum of those counts?
# Answer: 7653
# Time elapsed: 16.910554885864258 s

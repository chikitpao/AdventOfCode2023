""" Advent of Code 2023, Day 3
    Day 3: Gear Ratios
    Author: Chi-Kit Pao
"""

from collections import defaultdict
import os
import time


def get_surroundings(n, line_count, column_count):
    result = []

    check_left = False
    check_right = False
    check_up = False
    check_down = False
    if n[0] - 1 >= 0:
        check_up = True
    if n[0] + 1 < line_count:
        check_down = True
    if n[1] - 1 >= 0:
        check_left = True
    if n[1] + n[2] < column_count:
        check_right = True

    if check_up:
        if check_left:
            result.append((n[0] - 1, n[1] - 1))
        for i in range(n[2]):
            result.append((n[0] - 1, n[1] + i))
        if check_right:
            result.append((n[0] - 1, n[1] + n[2]))
    if check_left:
        result.append((n[0], n[1] - 1))
    if check_right:
        result.append((n[0], n[1] + n[2]))
    if check_down:
        if check_left:
            result.append((n[0] + 1, n[1] - 1))
        for i in range(n[2]):
            result.append((n[0] + 1, n[1] + i))
        if check_right:
            result.append((n[0] + 1, n[1] + n[2]))

    return result


def parse_numbers(line_number, line):
    result = []
    new_string = "".join(list(map(lambda c: c if c.isdigit() else " ", line)))
    for i in range(len(new_string) - 1):
        start_index = None
        if i == 0:
            if new_string[i].isdigit():
                start_index = 0
            elif not new_string[i].isdigit() and new_string[i + 1].isdigit():
                start_index = i + 1
        elif not new_string[i].isdigit() and new_string[i + 1].isdigit():
            start_index = i + 1
        if start_index is not None:
            try:
                index_ws = new_string[start_index:].index(" ")
                number = int(new_string[start_index : start_index + index_ws])
                result.append((line_number, start_index, index_ws, number))
            except ValueError:
                number = int(new_string[start_index:])
                result.append(
                    (line_number, start_index, len(new_string) - start_index, number)
                )
    return result


def parse_symbols(line_number, line):
    result = []
    for i, c in enumerate(list(line)):
        if c != "." and not c.isdigit():
            result.append((line_number, i, c))
    return result


def main():
    start_time = time.time()

    numbers = []
    symbols = dict()
    gears = defaultdict(set)

    file_path = os.path.dirname(__file__)
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
        for line_number, line in enumerate(lines):
            line_numbers = parse_numbers(line_number, line)
            numbers.extend(line_numbers)
            line_symbols = parse_symbols(line_number, line)
            for s in line_symbols:
                symbols[(s[0], s[1])] = s[2]

    result1 = 0
    for n in numbers:
        found_symbol = False
        surroundings = get_surroundings(n, len(lines), len(lines[0]))
        for s in surroundings:
            if s in symbols.keys():
                found_symbol = True
                symbol = symbols[s]
                if symbol == "*":
                    gears[s].add(n)

        if found_symbol:
            result1 += n[3]

    result2 = 0
    for v in gears.values():
        if len(v) == 2:
            l = list(v)
            result2 += l[0][3] * l[1][3]

    print(
        "Question 1: What is the sum of all of the part numbers in the engine schematic?"
    )
    print(f"Answer: {result1}")
    print("Question 2: What is the sum of all of the gear ratios in your engine schematic?")
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: What is the sum of all of the part numbers in the engine schematic?
# Answer: 539713
# Question 2: What is the sum of all of the gear ratios in your engine schematic?
# Answer: 84159075
# Time elapsed: 0.0 s

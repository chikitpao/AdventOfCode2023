""" Advent of Code 2023, Day 12
    Day 12: Hot Springs
    Author: Chi-Kit Pao
"""

import functools
import os
import time


def parse_line(line):
    pattern, p2 = line.split()
    number_values = eval(f"({p2})")
    return pattern, number_values


@functools.cache
def test_pattern(pattern, damages):
    result = 0
    current_damage = damages[0]
    remaining_damages = damages[1:]
    if len(remaining_damages) > 0:
        min_remaining_pattern_length = (
            sum(remaining_damages) + len(remaining_damages) - 1
        )
    else:
        min_remaining_pattern_length = 0
    for i in range(len(pattern) - current_damage - min_remaining_pattern_length + 1):
        if pattern[i] == "#":
            # Damage must start here.
            if all(map(lambda c: c in ("?", "#"), pattern[i : i + current_damage])):
                if len(remaining_damages) > 0:
                    if pattern[i + current_damage] in ("?", "."):
                        result += test_pattern(
                            pattern[i + current_damage + 1 :], remaining_damages
                        )
                else:
                    assert i + current_damage <= len(pattern)
                    if i + current_damage == len(pattern):
                        result += 1
                    else:
                        if all(
                            map(
                                lambda c: c in ("?", "."), pattern[i + current_damage :]
                            )
                        ):
                            result += 1
            break
        elif pattern[i] == "?":
            # Damage might start here.
            if all(map(lambda c: c in ("?", "#"), pattern[i : i + current_damage])):
                if len(remaining_damages) > 0:
                    if pattern[i + current_damage] in ("?", "."):
                        result += test_pattern(
                            pattern[i + current_damage + 1 :], remaining_damages
                        )
                else:
                    assert i + current_damage <= len(pattern)
                    if i + current_damage == len(pattern):
                        result += 1
                    else:
                        if all(
                            map(
                                lambda c: c in ("?", "."), pattern[i + current_damage :]
                            )
                        ):
                            result += 1
            continue
        else:
            # Found ".". Iterate further since damage doesn't start here.
            continue
    return result


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    # Part 1
    pattern_list = []
    damages_list = []
    for line in lines:
        pattern, damages = parse_line(line)
        pattern_list.append(pattern)
        damages_list.append(damages)

    result1 = 0
    for i in range(len(pattern_list)):
        temp = test_pattern(pattern_list[i], damages_list[i])
        result1 += temp

    # Part 2
    pattern_list2 = []
    damages_list2 = []
    for i in range(len(pattern_list)):
        pattern2 = (pattern_list[i] + "?") * 4 + pattern_list[i]
        pattern_list2.append(pattern2)
        damages2 = damages_list[i] * 5
        damages_list2.append(damages2)

    result2 = 0
    for i in range(len(pattern_list2)):
        temp = test_pattern(pattern_list2[i], damages_list2[i])
        result2 += temp

    print(
        "Question 1: For each row, count all of the different arrangements of\n"
        " operational and broken springs that meet the given criteria. What\n"
        " is the sum of those counts?"
    )
    print(f"Answer: {result1}")
    print(
        "Question 2: Unfold your condition records; what is the new sum of\n"
        " possible arrangement counts?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: For each row, count all of the different arrangements of
#  operational and broken springs that meet the given criteria. What
#  is the sum of those counts?
# Answer: 7653
# Question 2: Unfold your condition records; what is the new sum of
#  possible arrangement counts?
# Answer: 60681419004564
# Time elapsed: 0.455655574798584 s

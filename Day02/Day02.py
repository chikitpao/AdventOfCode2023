""" Advent of Code 2023, Day 2
    Day 2: Cube Conundrum
    Author: Chi-Kit Pao
"""

import math
import os
import re
import time


def check1(values):
    return all(map(lambda v: v[0] <= 12 and v[1] <= 13 and v[2] <= 14, values))


def power(values):
    min_count = [max(c) for c in zip(*values)]
    return math.prod(min_count)


def parse(line):
    p1, p2 = line.split(": ")
    _, nr = p1.split(" ")
    p2_list1 = p2.split("; ")
    p2_list = []
    for s1 in p2_list1:
        colors = ["red", "green", "blue"]
        values = [0, 0, 0]  # rgb
        comma_count = s1.count(",")
        groupdict = None
        if comma_count == 2:
            match = re.match(
                r"(?P<count1>\d+) (?P<color1>\w+), (?P<count2>\d+) (?P<color2>\w+), (?P<count3>\d+) (?P<color3>\w+)",
                s1,
            )
            groupdict = match.groupdict()
            count3 = int(groupdict["count3"])
            color3 = groupdict["color3"]
            values[colors.index(color3)] = count3
        if comma_count >= 1:
            if groupdict is None:
                match = re.match(
                    r"(?P<count1>\d+) (?P<color1>\w+), (?P<count2>\d+) (?P<color2>\w+)",
                    s1,
                )
                groupdict = match.groupdict()
            count2 = int(groupdict["count2"])
            color2 = groupdict["color2"]
            values[colors.index(color2)] = count2
        if comma_count >= 0:
            if groupdict is None:
                match = re.match(r"(?P<count1>\d+) (?P<color1>\w+)", s1)
                groupdict = match.groupdict()
            count1 = int(groupdict["count1"])
            color1 = groupdict["color1"]
            values[colors.index(color1)] = count1
        p2_list.append(values)
    return int(nr), p2_list


def main():
    start_time = time.time()

    file_path = os.path.dirname(__file__)
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
        values = dict()
        for line in lines:
            nr, p2 = parse(line)
            values[nr] = p2
        result1 = 0
        for k, v in values.items():
            if check1(v):
                result1 += k
        result2 = 0
        for k, v in values.items():
            result2 += power(v)

    print("Question 1: What is the sum of the IDs of those games?")
    print(f"Answer: {result1}")
    print("Question 2: What is the sum of the power of these sets?")
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: What is the sum of the IDs of those games?
# Answer: 2563
# Question 2: What is the sum of the power of these sets?
# Answer: 70768
# Time elapsed: 0.0 s

""" Advent of Code 2023, Day 4
    Day 4: Scratchcards
    Author: Chi-Kit Pao
"""

import os
import re
import time


def parse(line):
    p1, rest1 = line.split(": ")
    match = re.match(r"Card\s+(?P<card>\d+)", p1)
    groupdict = match.groupdict()
    card = int(groupdict["card"])

    p2, p3 = rest1.split(" | ")
    winning = []
    matches = re.findall(r"\s*(\d+)", p2)
    for match in matches:
        winning.append(int(match))
    own = []
    matches = re.findall(r"\s*(\d+)", p3)
    for match in matches:
        own.append(int(match))

    return card, winning, own


def main():
    start_time = time.time()

    file_path = os.path.dirname(__file__)
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    points = [0]
    result1 = 0
    for line in lines:
        _, winning, own = parse(line)
        inters = set(winning).intersection(own)
        l = len(inters)
        points.append(l)
        if l > 0:
            result1 += 2 ** (l - 1)

    card_count = [0] + [1] * (len(points) - 1)
    for i in range(1, len(points)):
        for j in range(i + 1, i + points[i] + 1):
            card_count[j] += card_count[i]
    result2 = sum(card_count)

    print("Question 1: How many points are they worth in total?")
    print(f"Answer: {result1}")
    print("Question 2: How many total scratchcards do you end up with?")
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: How many points are they worth in total?
# Answer: 20407
# Question 2: How many total scratchcards do you end up with?
# Answer: 23806951
# Time elapsed: 0.0 s

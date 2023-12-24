""" Advent of Code 2023, Day 24
    Day 24: Never Tell Me The Odds
    Author: Chi-Kit Pao
"""

import itertools
import numpy as np
import os
import time


def debug(*args):
    if True:
        print(*args)


class Hailstone:
    def __init__(self, id_, pos, v):
        self.id = id_
        self.pos = pos
        self.v = v


def parse_line(id_, line):
    # Example input
    # 230027994633462, 224850233272831, 164872865225455 @ 103, -57, 285
    p1, p2 = line.split(" @ ")
    pos = tuple([int(s) for s in p1.split(", ")])
    v = tuple([int(s) for s in p2.split(", ")])
    return Hailstone(id_, pos, v)


def part1(hailstones):
    total = 0
    for c in itertools.combinations(hailstones, 2):
        a = np.array([[c[0].v[0], - c[1].v[0]], [c[0].v[1], - c[1].v[1]]], dtype=np.int64)
        b = np.array([c[1].pos[0] - c[0].pos[0], c[1].pos[1] - c[0].pos[1]], dtype=np.int64)

        try:
            x = np.linalg.solve(a, b)
        except np.linalg.LinAlgError:
            continue

        if x[0] < 0 or x[1] < 0:
            continue
        intersection_x = c[0].pos[0] + x[0] * c[0].v[0]
        intersection_y = c[0].pos[1] + x[0] * c[0].v[1]
        if 200000000000000 <= intersection_x <= 400000000000000:
            if 200000000000000 <= intersection_y <= 400000000000000:
                total += 1
    return total


def main():
    start_time = time.time()

    hailstones = []

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    for i, line in enumerate(lines, 1):
        hailstones.append(parse_line(i, line))

    result1 = part1(hailstones)
    print(
        "Question 1: Considering only the X and Y axes, check all pairs of\n"
        " hailstones' future paths for intersections. How many of these\n"
        " intersections occur within the test area?"
    )
    print(f"Answer: {result1}")

    # result2 = 0
    # print(
    #    "Question 2: "
    # )
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Considering only the X and Y axes, check all pairs of
#  hailstones' future paths for intersections. How many of these
#  intersections occur within the test area?
# Answer: 20361
# Time elapsed: 0.4733572006225586 s

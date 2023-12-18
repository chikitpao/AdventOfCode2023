""" Advent of Code 2023, Day 18
    Day 18: Lavaduct Lagoon
    Author: Chi-Kit Pao
"""

import os
import re
import time


def get_wall(points, row, col):
    if (row, col) not in points:
        return "."

    muster = 0
    if (row - 1, col) in points:
        muster += 1
    if (row, col + 1) in points:
        muster += 2
    if (row + 1, col) in points:
        muster += 4
    if (row, col - 1) in points:
        muster += 8
    d = {3: "1", 6: "7", 12: "9", 9: "3", 5: "4", 10: "8"}
    try:
        return d[muster]
    except KeyError:
        print(row, col, KeyError, muster)


def count_enclosed_tiles(line):
    # Almost the same function as in Day 10
    inside_count = 0
    outside = True
    last_turn = None
    for tile in line:
        if tile == ".":
            if not outside:
                inside_count += 1
        elif tile == "4":  # vertical
            inside_count += 1
            outside = not outside
        elif tile == "8":  # horizontal
            inside_count += 1
        elif tile in ("7", "9", "1", "3"):
            inside_count += 1
            if last_turn is None:
                last_turn = tile
            else:
                # Orientation changed?
                changed = {"7": "3", "1": "9"}
                if tile == changed[last_turn]:
                    outside = not outside
                last_turn = None
    return inside_count


def main():
    start_time = time.time()
    points = set()
    coordinates = (0, 0)
    offsets = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    min_row = 0
    max_row = 0
    min_col = 0
    max_col = 0

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    for line in lines:
        match = re.match(r"(?P<dir>\w) (?P<length>\d+) \(#(?P<color>\w+)\)", line)
        groupdict = match.groupdict()
        dir = groupdict["dir"]
        length = int(groupdict["length"])
        color = int(groupdict["color"], 16)
        offset = offsets[dir]
        for _ in range(length):
            coordinates = tuple(map(sum, zip(coordinates, offset)))
            min_row = min(min_row, coordinates[0])
            max_row = max(max_row, coordinates[0])
            min_col = min(min_col, coordinates[1])
            max_col = max(max_col, coordinates[1])
            points.add(coordinates)

    # Part 1
    inside_count = 0
    for row in range(min_row, max_row + 1):
        s = "".join(
            [get_wall(points, row, col) for col in range(min_col - 1, max_col + 2)]
        )
        inside_count += count_enclosed_tiles(s)

    print(
        "Question 1: The Elves are concerned the lagoon won't be large\n"
        " enough; if they follow their dig plan, how many cubic meters of\n"
        " lava could it hold?"
    )
    print(f"Answer: {inside_count}")

    # Part 2
    # result2 = 0
    #print(
    #   "Question 2: Convert the hexadecimal color codes into the correct\n"
    #   " instructions; if the Elves follow this new dig plan, how many cubic\n"
    #   " meters of lava could the lagoon hold?"
    #)
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: The Elves are concerned the lagoon won't be large
#  enough; if they follow their dig plan, how many cubic meters of
#  lava could it hold?
# Answer: 67891
# Time elapsed: 0.03997921943664551 s

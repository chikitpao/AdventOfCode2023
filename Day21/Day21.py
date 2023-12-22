""" Advent of Code 2023, Day 21
    Day 21: Step Counter
    Author: Chi-Kit Pao
"""

import os
import time


class Map:
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def __init__(self, lines):
        self.map = []
        self.column_count = len(lines[0])
        self.row_count = len(lines)
        self.start_pos = None
        for line in lines:
            self.map.append("".join(["#" if c == "#" else " " for c in line]))
            if not self.start_pos:
                start = line.find("S")
                if start != -1:
                    self.start_pos = (len(self.map) - 1, start)


def part1(map_):
    offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    current_positions = {map_.start_pos}
    new_positions = set()
    for _ in range(64):
        for pos in current_positions:
            for i in range(4):
                test_pos = (pos[0] + offsets[i][0], pos[1] + offsets[i][1])
                if 0 <= test_pos[0] < map_.row_count:
                    if 0 <= test_pos[1] < map_.column_count:
                        if map_.map[test_pos[0]][test_pos[1]] != "#":
                            new_positions.add(test_pos)
        current_positions = new_positions
        new_positions = set()
    return len(current_positions)


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    map_ = Map(lines)
    result1 = part1(map_)
    print(
        "Question 1: Starting from the garden plot marked S on your map, how\n"
        " many garden plots could the Elf reach in exactly 64 steps?"
    )
    print(f"Answer: {result1}")

    # result2 = 0
    # print(
    #   "Question 2: However, the step count the Elf needs is much larger!\n"
    #   " Starting from the garden plot marked S on your infinite map, how many\n"
    #   " garden plots could the Elf reach in exactly 26501365 steps?"
    # )
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Starting from the garden plot marked S on your map, how
#  many garden plots could the Elf reach in exactly 64 steps?        
# Answer: 3737
# Time elapsed: 0.1129310131072998 s

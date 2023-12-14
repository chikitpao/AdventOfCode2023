""" Advent of Code 2023, Day 14
    Day 14: Parabolic Reflector Dish
    Author: Chi-Kit Pao
"""

import functools
import os
import time

@functools.cache
def line_hash(line):
    row_value = 0
    for i, c in enumerate(line):
        if c == "O":
            row_value += 2**i
    return row_value

class Map:
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def __init__(self, lines):
        self.cube_map = []
        self.round_map = []
        self.column_count = len(lines[0])
        self.row_count = len(lines)
        for line in lines:
            self.cube_map.append("".join(["#" if c == "#" else " " for c in line]))
            self.round_map.append(["O" if c == "O" else " " for c in line])

    def get_load(self):
        total = 0
        for i, line in enumerate(self.round_map):
            weight = self.row_count - i
            total += weight * line.count("O")
        return total
    
    def hash(self):
        l = []
        for line in self.round_map:
            l.append(line_hash("".join(line)))
        return tuple(l)

    def tilt(self, direction):
        if direction == Map.EAST or direction == Map.WEST:
            if direction == Map.EAST:
                delta = 1
                end = self.column_count
                gen = range(self.column_count - 2, -1, -1)
            else:
                delta = -1
                end = -1
                gen = range(1, self.column_count)
            for col in gen:
                for row in range(0, self.row_count):
                    if self.round_map[row][col] == "O":
                        self.__move_horizontally(row, col, delta, end)
            return

        if direction == Map.SOUTH or direction == Map.NORTH:
            if direction == Map.SOUTH:
                delta = 1
                end = self.row_count
                gen = range(self.row_count - 2, -1, -1)
            else:
                delta = -1
                end = -1
                gen = range(1, self.row_count)
            for row in gen:
                for col in range(0, self.column_count):
                    if self.round_map[row][col] == "O":
                        self.__move_vertically(row, col, delta, end)

    def __move_horizontally(self, row, col, delta, end):
        current = col
        while current + delta != end:
            if self.cube_map[row][current + delta] == "#":
                return
            if self.round_map[row][current + delta] == "O":
                return
            self.round_map[row][current + delta] = "O"
            self.round_map[row][current] = " "
            current += delta

    def __move_vertically(self, row, col, delta, end):
        current = row
        while current + delta != end:
            if self.cube_map[current + delta][col] == "#":
                return
            if self.round_map[current + delta][col] == "O":
                return
            self.round_map[current + delta][col] = "O"
            self.round_map[current][col] = " "
            current += delta


def part1(lines):
    map_ = Map(lines)
    map_.tilt(Map.NORTH)
    return map_.get_load()


def part2(lines):
    tilts = [Map.NORTH, Map.WEST, Map.SOUTH, Map.EAST]
    cycles = 1000000000
    history = dict()
    
    count = 0
    map_ = Map(lines)
    history[map_.hash()] = (0, map_.get_load())
    duplicate_count = None
    for _ in range(cycles):
        for tilt in tilts:
            map_.tilt(tilt)
        count += 1
        hash = map_.hash()
        if hash in history:
            duplicate_count = (history[hash][0], count)
            break
        else:
            history[hash] = (count, map_.get_load())
    else:
        # No cycle found (Hopefully we won't reach here ;-))
        return map_.get_load()
    
    remaining = (cycles - duplicate_count[0]) % (duplicate_count[1] - duplicate_count[0])
    result_index = duplicate_count[0] + remaining
    # Output: - Found cycle (103, 112). Result index 109.
    print(f"- Found cycle {duplicate_count}. Result index {result_index}.")
    for v in history.values():
        if v[0] == result_index:
            return v[1]
    return -1


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    result1 = part1(lines)
    print(
        "Question 1: Tilt the platform so that the rounded rocks all roll\n"
        " north. Afterward, what is the total load on the north support\n"
        " beams?"
    )
    print(f"Answer: {result1}")

    result2 = part2(lines)
    print(
       "Question 2: Run the spin cycle for 1000000000 cycles. Afterward,\n"
       " what is the total load on the north support beams?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Tilt the platform so that the rounded rocks all roll
#  north. Afterward, what is the total load on the north support
#  beams?
# Answer: 113424
# Question 2: Run the spin cycle for 1000000000 cycles. Afterward,
#  what is the total load on the north support beams?
# Answer: 96003
# Time elapsed: 1.1601369380950928 s

""" Advent of Code 2023, Day 16
    Day 16: The Floor Will Be Lava
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
        self.map = lines
        self.row_count = len(self.map)
        self.column_count = len(self.map[0])

    def track_beam(self, start_row, start_column, direction):
        beam_map = []
        for _ in range(self.row_count):
            beam_map.append([0] * self.column_count)
        params = self.__process_beam(beam_map, start_row, start_column, direction)
        while len(params) > 0:
            new_params = []
            for p in params:
                new_params.extend(self.__process_beam(beam_map, *p))
            params = new_params

        result = 0
        for row in beam_map:
            result += sum(map(lambda x: x > 0, row))
        return result

    def __process_beam(self, beam_map, prev_row, prev_col, direction):
        offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        current_row = prev_row + offsets[direction][0]
        current_col = prev_col + offsets[direction][1]
        if current_row < 0 or current_col < 0:
            return []
        if current_row >= self.row_count or current_col >= self.column_count:
            return []
        # Already visited in the same direction?
        if (beam_map[current_row][current_col] & (1 << direction)) != 0:
            return []
        beam_map[current_row][current_col] |= 1 << direction
        tile = self.map[current_row][current_col]
        if tile == ".":
            return [(current_row, current_col, direction)]
        elif tile == "|":
            if direction in (Map.EAST, Map.WEST):
                return [
                    (current_row, current_col, Map.NORTH),
                    (current_row, current_col, Map.SOUTH),
                ]
            else:
                return [(current_row, current_col, direction)]
        elif tile == "-":
            if direction in (Map.NORTH, Map.SOUTH):
                return [
                    (current_row, current_col, Map.EAST),
                    (current_row, current_col, Map.WEST),
                ]
            else:
                return [(current_row, current_col, direction)]
        elif tile == "/":
            next_directions = [Map.NORTH, Map.WEST, Map.SOUTH, Map.EAST]
            return [(current_row, current_col, next_directions[direction])]
        elif tile == "\\":
            next_directions = [Map.SOUTH, Map.EAST, Map.NORTH, Map.WEST]
            return [(current_row, current_col, next_directions[direction])]
        else:
            raise AssertionError(f"Unknown tile {tile}")
        return []


def part2(map_):
    result = 0
    for i in range(map_.row_count):
        result = max(result, map_.track_beam(i, -1, Map.EAST))
        result = max(result, map_.track_beam(i, map_.column_count, Map.WEST))
    for i in range(map_.column_count):
        result = max(result, map_.track_beam(-1, i, Map.SOUTH))
        result = max(result, map_.track_beam(map_.row_count, i, Map.NORTH))
    return result


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    map_ = Map(lines)

    result1 = map_.track_beam(0, -1, Map.EAST)
    print(
        "Question 1: With the beam starting in the top-left heading right,\n"
        " how many tiles end up being energized?"
    )
    print(f"Answer: {result1}")

    result2 = part2(map_)
    print(
        "Question 2: Find the initial beam configuration that energizes the\n"
        " largest number of tiles; how many tiles are energized in that\n"
        " configuration?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: With the beam starting in the top-left heading right,
#  how many tiles end up being energized?
# Answer: 7477
# Question 2: Find the initial beam configuration that energizes the
#  largest number of tiles; how many tiles are energized in that
#  configuration?
# Answer: 7853
# Time elapsed: 1.9994757175445557 s

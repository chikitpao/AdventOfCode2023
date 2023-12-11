""" Advent of Code 2023, Day 10
    Day 10: Pipe Maze
    Author: Chi-Kit Pao
"""

import os
import time


class Maze:
    def __init__(self, lines):
        self.map = lines
        self.simple_map = []
        self.row_count = len(self.map)
        self.col_count = len(self.map[0])
        self.loop = []

        # Find start position
        for row, line in enumerate(self.map):
            col = line.find("S")
            if col > -1:
                self.loop.append((row, col))
                break
        assert len(self.loop) == 1

        # Find loop
        self.step_count = 0
        previous_pos = None
        current_pos = self.loop[0]
        visited = set()
        visited.add(current_pos)
        start_replacement = None
        while True:
            next_positions = self.__get_next_positions(current_pos, previous_pos)
            if current_pos == self.loop[0]:
                if next_positions.count(None) != 2:
                    raise AssertionError("Start position doesn't have two neighbors!")
                start_replacement_index = sum(
                    [1 << i for i, x in enumerate(next_positions) if x is not None]
                )
                start_replacement = {3: "F", 6: "7", 9: "L", 12: "J"}[
                    start_replacement_index
                ]
            else:
                if next_positions.count(None) != 3:
                    raise AssertionError(
                        f"Got stuck! {current_pos} {self.map[next_pos[0]][next_pos[1]]} {next_positions}"
                    )
            self.step_count += 1
            next_pos = next(filter(lambda x: x is not None, next_positions))
            if next_pos == self.loop[0]:
                break
            if next_pos in visited:
                raise AssertionError(
                    f"Revisited position! {current_pos} {self.map[next_pos[0]][next_pos[1]]}"
                )
            visited.add(next_pos)
            previous_pos = current_pos
            current_pos = next_pos

        # Create simplified map for part two
        for row, line in enumerate(self.map):
            self.simple_map.append(["."] * self.col_count)
            for col in range(self.col_count):
                pos = (row, col)
                if pos in visited:
                    self.simple_map[row][col] = (
                        start_replacement if pos == self.loop[0] else self.map[row][col]
                    )

    def count_enclosed_tiles(self):
        inside_count = 0
        for line in self.simple_map:
            outside = True
            last_turn = None
            for tile in line:
                if tile == ".":
                    if not outside:
                        inside_count += 1
                elif tile == "|":
                    outside = not outside
                elif tile in ("J", "7", "L", "F"):
                    if last_turn is None:
                        last_turn = tile
                    else:
                        # Orientation changed?
                        changed = {"L": "7", "F": "J"}
                        if tile == changed[last_turn]:
                            outside = not outside
                        last_turn = None
        return inside_count

    def __get_next_positions(self, current_pos, previous_pos):
        """Returns coordinates of next positions [east, south, west, north]"""
        result = [None, None, None, None]
        offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for i, offset in enumerate(offsets):
            test_pos = (current_pos[0] + offset[0], current_pos[1] + offset[1])
            if previous_pos is not None and previous_pos == test_pos:
                continue
            if i == 0:  # east
                if test_pos[1] >= self.col_count:
                    continue
                if self.map[test_pos[0]][test_pos[1]] in ("S", "-", "J", "7"):
                    if self.map[current_pos[0]][current_pos[1]] in ("S", "-", "L", "F"):
                        result[i] = test_pos
            elif i == 1:  # south
                if test_pos[0] >= self.row_count:
                    continue
                if self.map[test_pos[0]][test_pos[1]] in ("S", "|", "L", "J"):
                    if self.map[current_pos[0]][current_pos[1]] in ("S", "|", "7", "F"):
                        result[i] = test_pos
            elif i == 2:  # west
                if test_pos[1] < 0:
                    continue
                if self.map[test_pos[0]][test_pos[1]] in ("S", "-", "L", "F"):
                    if self.map[current_pos[0]][current_pos[1]] in ("S", "-", "J", "7"):
                        result[i] = test_pos
            else:  # north
                if test_pos[0] < 0:
                    continue
                if self.map[test_pos[0]][test_pos[1]] in ("S", "|", "7", "F"):
                    if self.map[current_pos[0]][current_pos[1]] in ("S", "|", "L", "J"):
                        result[i] = test_pos

        return result


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    maze = Maze(lines)

    assert maze.step_count % 2 == 0
    result1 = maze.step_count // 2
    result2 = maze.count_enclosed_tiles()

    print(
        "Question 1: How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?"
    )
    print(f"Answer: {result1}")
    print("Question 2: How many tiles are enclosed by the loop?")
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
# Answer: 6968
# Question 2: How many tiles are enclosed by the loop?
# Answer:  413
# Time elapsed: 0.04077649116516113 s

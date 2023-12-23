""" Advent of Code 2023, Day 21
    Day 21: Step Counter
    Author: Chi-Kit Pao
"""

from collections import defaultdict
import os
import time


def debug(*args):
    if False:
        print(*args)


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


def project_position(map_, test_pos):
    # REMARK: Python % operator returns value with the same sign as demoninator
    # (unlike C or C++).
    row = test_pos[0]
    if row < 0 or row >= map_.row_count:
        row %= map_.row_count
    col = test_pos[1]
    if col < 0 or col >= map_.column_count:
        col %= map_.column_count
    return (row, col)

def reachable_position_count(last_count_in_maps, steps, map_):
    assert len(last_count_in_maps) % 2 == 1
    assert len(last_count_in_maps[0]) % 2 == 1
    assert len(last_count_in_maps) == len(last_count_in_maps[0])
    assert len(last_count_in_maps) >= 5  # Otherwise count in maps not stablized

    end_index = len(last_count_in_maps) - 1
    mid_index = (len(last_count_in_maps) - 1) // 2
    
    right_boundaries_count = (steps - (map_.column_count - 1 - map_.start_pos[1])) // map_.column_count + 1
    top1 = last_count_in_maps[0][mid_index]
    top2 = last_count_in_maps[1][mid_index]
    top3 = last_count_in_maps[2][mid_index]
    bottom = last_count_in_maps[end_index][mid_index]
    left = last_count_in_maps[mid_index][0]
    right = last_count_in_maps[mid_index][end_index]
    top_left1 = last_count_in_maps[0][mid_index - 1]
    top_left2 = last_count_in_maps[1][mid_index - 1]
    top_right1 = last_count_in_maps[0][mid_index + 1]
    top_right2 = last_count_in_maps[1][mid_index + 1]
    bottom_left1 = last_count_in_maps[end_index][mid_index - 1]
    bottom_left2 = last_count_in_maps[end_index - 1][mid_index - 1]
    bottom_right1 = last_count_in_maps[end_index][mid_index + 1]
    bottom_right2 = last_count_in_maps[end_index - 1][mid_index + 1]
    top2_count = (right_boundaries_count - 1) ** 2
    top3_count = (right_boundaries_count - 2) ** 2
    
    result = top1 + bottom + left + right
    result += (right_boundaries_count - 1) * (top_left1 + top_right1 + bottom_left1 + bottom_right1)
    result += (right_boundaries_count - 2) * (top_left2 + top_right2 + bottom_left2 + bottom_right2)
    result += top2_count * top2
    result += top3_count * top3
    return result


def part2(map_):
    offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # Actual positions
    current_positions = {map_.start_pos}
    new_positions = set()
    
    max_steps = 26501365
    # How many times we are going to reach right boundaries of map.
    # How many steps do we need after reaching right boundaries of map.
    remaining_steps = (max_steps - (map_.column_count - 1 - map_.start_pos[1])) % map_.column_count
    # Output:
    # remaining_steps 0
    debug(f"remaining_steps {remaining_steps}")
    
    milestones = [i * map_.column_count - 1 - map_.start_pos[1] + remaining_steps for i in range(1, 4)]
    last_correct_step = 2
    last_count_in_maps = []
    for steps in range(1, milestones[-1] + 1):
        is_milestone = steps in milestones
        map_y_boundries = [0, 0]
        map_x_boundries = [0, 0]
        count_in_maps = defaultdict(int)
        for pos in current_positions:
            for dir in range(4):
                test_pos = (pos[0] + offsets[dir][0], pos[1] + offsets[dir][1])
                projected_pos = project_position(map_, test_pos)
                if map_.map[projected_pos[0]][projected_pos[1]] != "#":
                    if not is_milestone:
                        new_positions.add(test_pos)
                    elif test_pos not in new_positions:
                        map_y = (test_pos[0] - (test_pos[0] % map_.row_count)) // map_.row_count
                        map_x = (test_pos[1] - (test_pos[1] % map_.column_count)) // map_.column_count
                        map_y_boundries[0], map_y_boundries[1] = min(map_y_boundries[0], map_y), max(map_y_boundries[1], map_y)
                        map_x_boundries[0], map_x_boundries[1] = min(map_x_boundries[0], map_x), max(map_x_boundries[1], map_x)
                        count_in_maps[(map_y, map_x)] += 1
                        new_positions.add(test_pos)
        if is_milestone:
            # Output:
            # steps 65 count 4001
            # steps 196 count 34928
            # steps 327 count 96417
            # steps 458 count 188468
            # steps 589 count 311081
            # steps 720 count 464256
            debug(f"steps {steps} count {len(new_positions)}")
            for y in range(map_y_boundries[0], map_y_boundries[1] + 1):
                debug([f"{count_in_maps[(y, x)]:>4}" for x in range(map_x_boundries[0], map_x_boundries[1] + 1)])
            if steps == milestones[last_correct_step]:
                for y in range(map_y_boundries[0], map_y_boundries[1] + 1):
                    last_count_in_maps.append([count_in_maps[(y, x)] for x in range(map_x_boundries[0], map_x_boundries[1] + 1)])

        new_positions, current_positions = current_positions, new_positions
        new_positions.clear()

    return reachable_position_count(last_count_in_maps, max_steps, map_)


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    map_ = Map(lines)

    # Output: 
    # Dimension: (131, 131)
    # Start position: (65, 65))
    debug(f"Dimension: ({map_.row_count}, {map_.column_count})")
    debug(f"Start position: {map_.start_pos}")
    # Assert map is quadratic:
    map_.row_count == map_.column_count 
    # Assert start position is centric:
    assert map_.start_pos[0] - 0 == map_.row_count - 1 - map_.start_pos[0]
    assert map_.start_pos[1] - 0 == map_.column_count - 1 - map_.start_pos[1]
    # Assert these rows are empty
    for row in (0, map_.start_pos[0], map_.row_count - 1):
        assert all(map(lambda c: c == " ", map_.map[row]))
    # Assert these columns are empty
    for col in (0, map_.start_pos[1], map_.column_count - 1):
        column = [row[col] for row in map_.map]
        assert all(map(lambda c: c == " ", column))

    result1 = part1(map_)
    print(
        "Question 1: Starting from the garden plot marked S on your map, how\n"
        " many garden plots could the Elf reach in exactly 64 steps?"
    )
    print(f"Answer: {result1}")

    result2 = part2(map_)
    print(
        "Question 2: However, the step count the Elf needs is much larger!\n"
        " Starting from the garden plot marked S on your infinite map, how many\n"
        " garden plots could the Elf reach in exactly 26501365 steps?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Starting from the garden plot marked S on your map, how
#  many garden plots could the Elf reach in exactly 64 steps?
# Answer: 3737
# Question 2: However, the step count the Elf needs is much larger!
#  Starting from the garden plot marked S on your infinite map, how many
#  garden plots could the Elf reach in exactly 26501365 steps?
# Answer: 625382480005896
# Time elapsed: 28.80467963218689 s

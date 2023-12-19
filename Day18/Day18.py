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


def parse_input():
    data = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    for line in lines:
        match = re.match(r"(?P<dir>\w) (?P<length>\d+) \(#(?P<color>\w+)\)", line)
        groupdict = match.groupdict()
        dir = groupdict["dir"]
        length = int(groupdict["length"])
        color = groupdict["color"]
        length2 = int(color[:5], 16)
        dir_dict =  {0: "R", 1: "D", 2: "L", 3: "U"}
        dir2 = dir_dict[int(color[5])]
        data.append((dir, length, dir2, length2))
    return data


def part1(data):
    points = set()
    # Screen coordinates
    offsets = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    coordinates = (0, 0)
    min_row = 0
    max_row = 0
    min_col = 0
    max_col = 0

    for d in data:
        offset = offsets[d[0]]
        for _ in range(d[1]):
            coordinates = tuple(map(sum, zip(coordinates, offset)))
            min_row = min(min_row, coordinates[0])
            max_row = max(max_row, coordinates[0])
            min_col = min(min_col, coordinates[1])
            max_col = max(max_col, coordinates[1])
            points.add(coordinates)

    inside_count = 0
    for row in range(min_row, max_row + 1):
        s = "".join(
            [get_wall(points, row, col) for col in range(min_col - 1, max_col + 2)]
        )
        inside_count += count_enclosed_tiles(s)
    return inside_count


def part2(data):
    # Cartesian coordinates
    offsets = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    positions = []
    current_pos = (0, 0)
    perimeter = 0
    cw_turn_count = 0
    ccw_turn_count = 0

    def orientation(dir, next_dir):
        cw_turns = (("U", "R"), ("R", "D"), ("D", "L"), ("L", "U"))
        if (dir, next_dir) in cw_turns:
            return True
        if (next_dir, dir) in cw_turns:
            return False
        assert "Not a turn!"

    data_count = len(data)
    positions.append(current_pos)
    for i in range(data_count):
        d = data[i]
        offset = offsets[d[2]]
        length = d[3]
        perimeter += length
        next_dir = data[0][2] if i + 1 == data_count else data[i + 1][2]
        if orientation(d[2], next_dir):
            cw_turn_count += 1
        else:
            ccw_turn_count += 1
        x = current_pos[0] + length * offset[0]
        y = current_pos[1] + length * offset[1]
        current_pos = (x, y)
        positions.append(current_pos)

    # Finally we shall arrive at start position.
    assert current_pos == (0, 0), f"current_pos {current_pos}"

    # There shall be four exterior corners more than interior corners.
    # If we travel counter-clockwise, then clockwise turns are exterior and
    # counter-clockwise turns interior. (Clockwise turns interior /
    # counter-clockwise turns exterior when traveling clockwise)
    assert abs(cw_turn_count - ccw_turn_count) == 4

    # With the Shoelace formula, we will get the area inside the exact
    # coordinates.
    temp = 0
    for i in range(len(positions) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        temp += x1 * y2 - x2 * y1
    area_by_shoelace = abs(temp) / 2

    # But since we also need the sqaure area around the exact coordinates, we
    # need to add 1/2 for horizontal or vertical square, add 3/4 for an exterior
    # corner and 1/4 for an interior corner.
    # Or we can add 1/2 for every square we have visited and plus 1/4 for every
    # exterior corner and minus 1/4 for every interior corner.
    # Since there are always four exterior corners more than interior corners,
    # we can add 1/2 for every square we have visited and plus 1
    # (= 4 * 1/4).
    return int(area_by_shoelace + perimeter / 2 + 1)


def main():
    start_time = time.time()
    data = parse_input()

    result1 = part1(data)
    print(
        "Question 1: The Elves are concerned the lagoon won't be large\n"
        " enough; if they follow their dig plan, how many cubic meters of\n"
        " lava could it hold?"
    )
    print(f"Answer: {result1}")

    result2 = part2(data)
    print(
        "Question 2: Convert the hexadecimal color codes into the correct\n"
        " instructions; if the Elves follow this new dig plan, how many cubic\n"
        " meters of lava could the lagoon hold?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: The Elves are concerned the lagoon won't be large
#  enough; if they follow their dig plan, how many cubic meters of
#  lava could it hold?
# Answer: 67891
# Question 2: Convert the hexadecimal color codes into the correct
#  instructions; if the Elves follow this new dig plan, how many cubic
#  meters of lava could the lagoon hold?
# Answer: 94116351948493
# Time elapsed: 0.0704808235168457 s

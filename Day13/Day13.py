""" Advent of Code 2023, Day 12
    Day 12: Hot Springs
    Author: Chi-Kit Pao
"""

import os
import time


class Map:
    def __init__(self):
        self.lines = []
        pass

    def find_mirror(self):
        column_count = len(self.lines[0])
        row_values = []
        tile = lambda c: 1 if c == "#" else 0
        for line in self.lines:
            row_values.append(sum([tile(c) * 2**i for i, c in enumerate(line)]))
            pass
        column_values = []
        for col in range(column_count):
            column_values.append(
                sum([tile(line[col]) * 2**i for i, line in enumerate(self.lines)])
            )
        return self.find_mirror_ex(row_values), self.find_mirror_ex(column_values)

    def find_mirror_ex(self, values):
        for i in range(len(values) - 1):
            if values[i] != values[i + 1]:
                continue
            items_to_check = min(i + 1, len(values) - i - 1)
            if (
                list(reversed(values[i - items_to_check + 1 : i + 1]))
                == values[i + 1 : i + 1 + items_to_check]
            ):
                return i + 1
        return 0


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    maps = []
    current_map = None
    for line in lines:
        if len(line) > 0:
            if current_map is None:
                current_map = Map()
            current_map.lines.append(line)
        else:
            # Append map when encountered empty line.
            maps.append(current_map)
            current_map = None
    # Append map at the end of file (when there is no empty line).
    if current_map is not None:
        maps.append(current_map)

    # Part 1
    result1 = 0
    for map_ in maps:
        row, column = map_.find_mirror()
        assert (row, column).count(0) == 1
        result1 += row * 100 + column

    # Part2
    # result2 = 0

    print(
        "Question 1: Find the line of reflection in each of the patterns in\n"
        " your notes. What number do you get after summarizing all of your\n"
        " notes?"
    )
    print(f"Answer: {result1}")
    print(
       "Question 2: In each pattern, fix the smudge and find the different\n"
       " line of reflection. What number do you get after summarizing the\n"
       " new reflection line in each pattern in your notes?"
    )
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Find the line of reflection in each of the patterns in
#  your notes. What number do you get after summarizing all of your
#  notes?
# Answer: 31956
# Time elapsed: 0.013921737670898438 s

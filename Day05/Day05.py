""" Advent of Code 2023, Day 5
    Day 5: If You Give A Seed A Fertilizer
    Author: Chi-Kit Pao
"""

import itertools
import os
import re
import time


def parse_seeds(lines, start_index):
    result = []
    _, p2 = lines[0].split(":")
    matches = re.findall(r"\s*(\d+)", p2)
    for match in matches:
        result.append(int(match))
    return result, start_index + 2


def parse_map(lines, start_index):
    current_index = start_index + 1
    line_parsed = 1
    result = []
    while current_index < len(lines) and len(lines[current_index]) > 0:
        match = re.match(
            r"(?P<dest>\d+) (?P<src>\d+) (?P<length>\d+)", lines[current_index]
        )
        groupdict = match.groupdict()
        dest = int(groupdict["dest"])
        src = int(groupdict["src"])
        length = int(groupdict["length"])
        result.append((src, dest, length, src + length))
        current_index += 1
        line_parsed += 1
    result.sort()
    return result, (line_parsed + 1)


class Map:
    def __init__(self, conversions):
        self.conversions = conversions

    def calc(self, n):
        for c in self.conversions:
            if c[0] <= n < c[0] + c[2]:
                return c[1] + n - c[0]
        return n

    def calc_ranges(self, ranges):
        result = []
        for r in ranges:
            result.extend(self.__calc_range(r))
        return result

    def __calc_range(self, r):
        start, end_excl = r[0], r[1]
        current_conversions = list(
            itertools.takewhile(
                lambda c2: c2[0] < end_excl,
                itertools.dropwhile(
                    lambda c1: c1[0] + c1[2] <= start, self.conversions
                ),
            )
        )
        current_conversion_count = len(current_conversions)
        assert current_conversion_count > 0
        result = []
        if current_conversion_count == 1:
            offset = current_conversions[0][1] - current_conversions[0][0]
            result.append((r[0] + offset, r[1] + offset))
        else:
            first_offset = current_conversions[0][1] - current_conversions[0][0]
            result.append(
                (r[0] + first_offset, current_conversions[0][3] + first_offset)
            )

            if current_conversion_count > 2:
                for i in range(1, current_conversion_count - 1):
                    offset = current_conversions[i][1] - current_conversions[i][0]
                    result.append(
                        (
                            current_conversions[i][0] + offset,
                            current_conversions[i][3] + offset,
                        )
                    )

            last_offset = current_conversions[-1][1] - current_conversions[-1][0]
            result.append(
                (current_conversions[-1][0] + last_offset, r[1] + last_offset)
            )
        return result


def part1(seeds, maps):
    locations = []
    for s in seeds:
        value = s
        for m in maps:
            value = m.calc(value)
        locations.append(value)
    locations.sort()
    return locations[0]


def part2(seeds, maps):
    min_value = None
    for i in range(0, len(seeds), 2):
        values = [(seeds[i], seeds[i] + seeds[i + 1])]  # [start, end)
        for m in maps:
            new_values = m.calc_ranges(values)
            values = new_values
        assert len(values) > 0
        values.sort()
        if min_value is None:
            min_value = values[0]
        elif values[0] < min_value:
            min_value = values[0]
    return min_value[0]


def main():
    start_time = time.time()

    file_path = os.path.dirname(__file__)
    maps = []
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
        start_line = 0

        seeds, lines_read = parse_seeds(lines, start_line)
        start_line += lines_read

        end_exclusive = 0
        for i in range(7):
            m, lines_read = parse_map(lines, start_line)
            print(i, m[0][0], m[-1][-1])
            assert m[0][0] == 0
            end_exclusive = max(end_exclusive, m[-1][-1])
            # Fill gaps in between for easier handling
            gaps = []
            for j in range(len(m) - 1):
                if m[j][-1] != m[j + 1][0]:
                    gaps.append(
                        (m[j][-1], m[j][-1], m[j + 1][0] - m[j][-1], m[j + 1][0])
                    )
            if len(gaps) > 0:
                m.extend(gaps)
                m.sort()
            maps.append(Map(m))
            start_line += lines_read
        # Fill gaps at the end
        for mo in maps:
            m = mo.conversions
            if m[-1][-1] < end_exclusive:
                m.append(
                    (m[-1][-1], m[-1][-1], end_exclusive - m[-1][-1], end_exclusive)
                )

        for i in range(0, len(seeds), 2):
            print("seed", (seeds[i], seeds[i] + seeds[i + 1]))
            assert seeds[i] + seeds[i + 1] < end_exclusive

    print(
        "Question 1: What is the lowest location number that corresponds to any of the initial seed numbers?"
    )
    print(f"Answer: {part1(seeds, maps)}")
    print(
        "Question 2: What is the lowest location number that corresponds to any of the initial seed numbers?"
    )
    print(f"Answer: {part2(seeds, maps)}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: What is the lowest location number that corresponds to any of the initial seed numbers?
# Answer: 579439039
# Question 2: What is the lowest location number that corresponds to any of the initial seed numbers?
# Answer: 7873084
# Time elapsed: 0.001976490020751953 s

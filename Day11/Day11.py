""" Advent of Code 2023, Day 11
    Day 11: Cosmic Expansion
    Author: Chi-Kit Pao
"""

import itertools
import os
import time


def get_sum(galaxies, empty_rows, empty_columns, factor):
    total = 0
    for c in itertools.combinations(galaxies, 2):
        y1, x1 = c[0]
        y2, x2 = c[1]
        dx = abs(x2 - x1)
        if x1 > x2:
            x2, x1 = x1, x2
        dx += (factor - 1) * len(
            list(
                itertools.takewhile(
                    lambda x: x < x2,
                    itertools.dropwhile(lambda x: x < x1, empty_columns),
                )
            )
        )
        dy = abs(y2 - y1)
        if y1 > y2:
            y2, y1 = y1, y2
        dy += (factor - 1) * len(
            list(
                itertools.takewhile(
                    lambda y: y < y2, itertools.dropwhile(lambda y: y < y1, empty_rows)
                )
            )
        )
        total += dx + dy
    return total


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    empty_rows = []
    empty_columns = []
    row_count = len(lines[0])
    column_count = len(lines[0])
    galaxies = []
    for row, line in enumerate(lines):
        row_galaxies = []
        for col in range(column_count):
            if line[col] == "#":
                row_galaxies.append((row, col))
        if len(row_galaxies) == 0:
            empty_rows.append(row)
        else:
            galaxies.extend(row_galaxies)
    for col in range(column_count):
        for row in range(row_count):
            if lines[row][col] == "#":
                break
        else:
            empty_columns.append(col)

    result1 = get_sum(galaxies, empty_rows, empty_columns, 2)
    result2 = get_sum(galaxies, empty_rows, empty_columns, 10**6)

    print(
        "Question 1: Expand the universe, then find the length of the shortest \n"
        " path between every pair of galaxies. What is the sum of these lengths?"
    )
    print(f"Answer: {result1}")
    print(
        "Question 2: Starting with the same initial image, expand the universe\n"
        " according to these new rules, then find the length of the shortest\n"
        " path between every pair of galaxies. What is the sum of these lengths?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()


# Question 1: Expand the universe, then find the length of the shortest 
#  path between every pair of galaxies. What is the sum of these lengths?
# Answer: 9177603
# Question 2: Starting with the same initial image, expand the universe
#  according to these new rules, then find the length of the shortest
#  path between every pair of galaxies. What is the sum of these lengths?
# Answer: 632003913611
# Time elapsed: 0.411482572555542 s

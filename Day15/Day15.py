""" Advent of Code 2023, Day 15
    Day 15: Lens Library
    Author: Chi-Kit Pao
"""

import os
import time


def hash(token):
    result = 0
    for c in token:
        result += ord(c)
        result *= 17
        result %= 256
    return result


def part2(tokens):
    boxes = []
    for _ in range(256):
        boxes.append([])
    for token in tokens:
        end = next(i for i, v in enumerate(token) if v in ("-", "="))
        box_index = hash(token[:end])
        try:
            char_pos = token.index("-")
            label = token[:char_pos]
            lens_index = next(
                (i for i, v in enumerate(boxes[box_index]) if v[0] == label), -1
            )
            if lens_index != -1:
                boxes[box_index].pop(lens_index)
        except ValueError:
            char_pos = token.index("=")
            label, value = token[:char_pos], int(token[char_pos + 1 :])
            lens_index = next(
                (i for i, v in enumerate(boxes[box_index]) if v[0] == label), -1
            )
            if lens_index != -1:
                boxes[box_index][lens_index][1] = value
            else:
                boxes[box_index].append([label, value])
    result = 0
    for i, box in enumerate(boxes, 1):
        for j, lens in enumerate(box, 1):
            # print(i, j, lens[1])
            result += i * j * lens[1]
    return result


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    assert len(lines) == 1
    tokens = lines[0].split(",")

    result1 = sum([hash(token) for token in tokens])
    print(
        "Question 1: Run the HASH algorithm on each step in the initialization\n"
        " sequence. What is the sum of the results?"
    )
    print(f"Answer: {result1}")

    result2 = part2(tokens)
    print(
        "Question 2: With the help of an over-enthusiastic reindeer in a hard\n"
        " hat, follow the initialization sequence. What is the focusing power\n"
        " of the resulting lens configuration?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Run the HASH algorithm on each step in the initialization
#  sequence. What is the sum of the results?
# Answer: 507291
# Question 2: With the help of an over-enthusiastic reindeer in a hard
#  hat, follow the initialization sequence. What is the focusing power
#  of the resulting lens configuration?
# Answer: 296921
# Time elapsed: 0.012195587158203125 s

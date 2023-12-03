""" Advent of Code 2023, Day 1
    Day 1: Trebuchet?!
    Author: Chi-Kit Pao
"""

import os
import time


def parse1(line):
    digits = list(filter(lambda c: c.isdigit(), list(line)))
    return (ord(digits[0]) - ord("0")) * 10 + ord(digits[-1]) - ord("0")


def parse2(line):
    digits = [(i, ord(c) - ord("0")) for i, c in enumerate(list(line)) if c.isdigit()]
    digit_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for digit, word in enumerate(digit_words, 1):
        digits.extend([(i, digit) for i in range(len(line)) if line[i: i + len(word)] == word])
    digits.sort()
    return digits[0][1] * 10 + digits[-1][1]


def main():
    start_time = time.time()

    file_path = os.path.dirname(__file__)
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
        result1 = 0
        result2 = 0
        for line in lines:
            result1 += parse1(line)
            result2 += parse2(line)

    print("Question 1: What is the sum of all of the calibration values?")
    print(f"Answer: {result1}")
    print("Question 2: What is the sum of all of the calibration values?")
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: What is the sum of all of the calibration values?
# Answer: 53974
# Question 2: What is the sum of all of the calibration values?
# Answer: 52840
# Time elapsed: 0.03156447410583496 s

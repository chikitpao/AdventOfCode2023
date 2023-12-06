""" Advent of Code 2023, Day 6
    Day 6: Wait For It
    Author: Chi-Kit Pao
"""

import math
import time


def winning_count(time_, distance):
    count = [0] * (time_ + 1)
    for i in range(0, time_ + 1):
        count[i] = (time_ - i) * i

    return sum(map(lambda x: x > distance, count))


def part1(races):
    return math.prod([winning_count(t, d) for t, d in races])


def main():
    start_time = time.time()

    #  Time-Distance pairs
    races = [(46, 208), (85, 1412), (75, 1257), (82, 1410)]
    race2 = (46857582, 208141212571410)

    print(
        "Question 1: Determine the number of ways you could beat the record "
        "in each race. What do you get if you multiply these numbers "
        "together?"
    )
    print(f"Answer: {part1(races)}")
    print("How many ways can you beat the record in this one much longer race?")
    print(f"Answer: {winning_count(race2[0], race2[1])}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()


# Question 1: Determine the number of ways you could beat the record in each race. "
# "What do you get if you multiply these numbers together?
# Answer: 1108800
# How many ways can you beat the record in this one much longer race?
# Answer: 36919753
# Time elapsed: 7.161836862564087 s

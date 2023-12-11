""" Advent of Code 2023, Day 9
    Day 9: Mirage Maintenance
    Author: Chi-Kit Pao
"""

import os
import time


def extrapolate(in_list):
    assert len(in_list) >= 1
    if all(map(lambda x: x == in_list[0], in_list)):
        out_list = in_list.copy()
        out_list.insert(0, in_list[0])
        out_list.append(in_list[-1])
        return out_list
    temp_in_list = [in_list[i + 1] - in_list[i] for i in range(len(in_list) - 1)]
    temp_out_list = extrapolate(temp_in_list)
    out_list = in_list.copy()
    out_list.insert(0, in_list[0] - temp_out_list[0])
    out_list.append(in_list[-1] + temp_out_list[-1])
    return out_list


def main():
    start_time = time.time()
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    data = []
    for line in lines:
        data.append(list(map(int, line.split())))

    result1 = 0
    result2 = 0
    for d in data:
        values = extrapolate(d)
        result1 += values[-1]
        result2 += values[0]

    print("Question 1: What is the sum of these extrapolated next values?")
    print(f"Answer: {result1}")
    print("Question 2: What is the sum of these extrapolated previous values?")
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: What is the sum of these extrapolated next values?
# Answer: 2038472161
# Question 2: What is the sum of these extrapolated previous values?
# Answer: 1091
# Time elapsed: 0.015643596649169922 s

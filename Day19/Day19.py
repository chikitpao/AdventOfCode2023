""" Advent of Code 2023, Day 19
    Day 19: Aplenty
    Author: Chi-Kit Pao
"""

import os
import re
import time


class Rule:
    def __init__(self, name, rules):
        assert len(rules) > 1
        assert rules[-1].find(":") == -1
        self.name = name
        self.default_rule = rules[-1]
        self.rules = []
        for rule in rules[: len(rules) - 1]:
            match = re.match(
                r"(?P<lhs>[xmas])(?P<op>[<>])(?P<rhs>\d+):(?P<out>\w+)", rule
            )
            groupdict = match.groupdict()
            lhs = groupdict["lhs"]
            lhs_dict = {"x": 0, "m": 1, "a": 2, "s": 3}
            lhs_index = lhs_dict[lhs]
            op = groupdict["op"]
            rhs = int(groupdict["rhs"])
            out = groupdict["out"]
            self.rules.append((lhs_index, op, rhs, out))

    def op(self, part):
        for lhs_index, op, rhs, out in self.rules:
            lhs = part[lhs_index]
            if op == ">" and lhs > rhs:
                return out
            elif op == "<" and lhs < rhs:
                return out
        return self.default_rule


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    rule_objs = dict()
    parts = []
    is_rule = True
    for line in lines:
        if is_rule:
            # Rules
            if len(line) == 0:
                is_rule = False
                continue
            # Example input:
            # px{a<2006:qkq,m>2090:A,rfg}
            sb = line.find("{")
            eb = line.find("}")
            assert -1 not in (sb, eb)
            name = line[:sb]
            rules_str = line[sb + 1 : eb]
            rules = rules_str.split(",")
            rule_objs[name] = Rule(name, rules)
        else:
            # Parts
            # Example input:
            # {x=1853,m=1718,a=852,s=421}
            match = re.match(
                r"\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)\}", line
            )
            groupdict = match.groupdict()
            x = int(groupdict["x"])
            m = int(groupdict["m"])
            a = int(groupdict["a"])
            s = int(groupdict["s"])
            parts.append((x, m, a, s))
    return rule_objs, parts


def part1(rule_objs, parts):
    result = 0
    for part in parts:
        response = rule_objs["in"].op(part)
        while response not in ("A", "R"):
            response = rule_objs[response].op(part)
        if response == "A":
            result += sum(part)
    return result


def main():
    start_time = time.time()
    rule_objs, parts = parse_input()

    result1 = part1(rule_objs, parts)
    print(
        "Question 1: Sort through all of the parts you've been given; what\n"
        " do you get if you add together all of the rating numbers for all\n"
        " of the parts that ultimately get accepted?"
    )
    print(f"Answer: {result1}")

    # result2 = part2(rule_objs, parts)
    # print(
    #     "Question 2: Consider only your list of workflows; the list of part\n"
    #     " ratings that the Elves wanted you to sort is no longer relevant.\n"
    #     " How many distinct combinations of ratings will be accepted by the\n"
    #     " Elves' workflows?"
    # )
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Sort through all of the parts you've been given; what
#  do you get if you add together all of the rating numbers for all
#  of the parts that ultimately get accepted?
# Answer: 432788
# Time elapsed: 0.0 s

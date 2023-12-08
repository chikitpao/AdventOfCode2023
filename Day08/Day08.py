""" Advent of Code 2023, Day 8
    Day 8: Haunted Wasteland
    Author: Chi-Kit Pao
"""

import math
import os
import re
import sympy as sp
import time


class Map:
    def __init__(self, lines):
        self.instructions = lines[0]
        self.ip = 0
        self.graph = dict()
        for line in lines[2:]:
            match = re.match(r"(?P<node>\w+) = \((?P<left>\w+), (?P<right>\w+)\)", line)
            groupdict = match.groupdict()
            node = groupdict["node"]
            left = groupdict["left"]
            right = groupdict["right"]
            self.graph[node] = (left, right)

    def get_answer1(self):
        steps = 0
        currentNode = "AAA"
        while True:
            instruction = self.instructions[self.ip]
            neighbors = self.graph[currentNode]
            currentNode = neighbors[0] if instruction == "L" else neighbors[1]
            steps += 1
            self.ip = (self.ip + 1) % len(self.instructions)
            if currentNode == "ZZZ":
                return steps

    def get_answer2(self):
        currentNodes = [node for node in self.graph.keys() if node.endswith("A")]
        total_potential_goal_steps = [None] * len(currentNodes)
        cycle_length = [None] * len(currentNodes)

        for i, startNode in enumerate(currentNodes):
            currentNode = startNode
            potential_goal_steps = []
            steps = 0
            while True:
                instruction = self.instructions[self.ip]
                neighbor_index = 0 if instruction == "L" else 1
                currentNode = self.graph[currentNode][neighbor_index]
                steps += 1
                self.ip = (self.ip + 1) % len(self.instructions)
                if currentNode[2] == "Z":
                    finished = False
                    if any(map(lambda s: s[0] == currentNode, potential_goal_steps)):
                        finished = True
                    potential_goal_steps.append((currentNode, steps))
                    # Ends by revisiting a potential goal
                    # Every start node only has one potential goal.
                    if finished == True:
                        total_potential_goal_steps[i] = potential_goal_steps
                        break
                elif currentNode == startNode:
                    # Ends with stepping on start node again
                    # => Didn't happen with my input.
                    cycle_length[i] = steps
                    total_potential_goal_steps[i] = potential_goal_steps
                    break
        # My outputs:
        # len(self.instructions): 263
        # cycle_length: [None, None, None, None, None, None]
        # total_potential_goal_steps:  [[('HMZ', 20777), ('HMZ', 41554)],
        #  [('ZZZ', 18673), ('ZZZ', 37346)], [('RNZ', 13939), ('RNZ', 27878)],
        #  [('XKZ', 17621), ('XKZ', 35242)], [('LFZ', 19199), ('LFZ', 38398)],
        #  [('DDZ', 12361), ('DDZ', 24722)]]
        print("len(self.instructions):", len(self.instructions))
        print("cycle_length:", cycle_length)
        print("total_potential_goal_steps: ", total_potential_goal_steps)
        assert sp.isprime(len(self.instructions))

        for i, pgs in enumerate(total_potential_goal_steps):
            assert (pgs[1][1] - pgs[0][1]) % len(self.instructions) == 0
            # My outputs:
            # 79 0 79
            # 71 0 71
            # 53 0 53
            # 67 0 67
            # 73 0 73
            # 47 0 47
            a = pgs[0][1] // len(self.instructions)
            b = pgs[0][1] % len(self.instructions)
            c = (pgs[1][1] - pgs[0][1]) // len(self.instructions)
            print(a, b, c)
            assert a == c
            assert b == 0
            assert sp.isprime(c)
            pgs[0][1] % len(self.instructions)

        instructions_length = len(self.instructions)
        total_potential_goal_cycles = []
        for c in total_potential_goal_steps:
            temp = [
                (c[0][1] // instructions_length),
                ((c[1][1] - c[0][1]) // instructions_length),
            ]
            total_potential_goal_cycles.append(temp)
        # My outputs:
        # [[79, 79], [71, 71], [53, 53], [67, 67], [73, 73], [47, 47]]
        print(total_potential_goal_cycles)

        # 1: Find pairwise multiple cycles
        pairwise_multiple_cycles = []
        for i in range(0, len(total_potential_goal_cycles), 2):
            pgc1 = total_potential_goal_cycles[i]
            pgc2 = total_potential_goal_cycles[i + 1]
            pairwise_multiple_cycles.append(pgc1[0] + (pgc2[1] - 1) * pgc1[1])
        # 2: Find LCM of these cycles
        lcm = math.lcm(*pairwise_multiple_cycles)
        return lcm * instructions_length


def main():
    start_time = time.time()
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    quiz_map = Map(lines)

    print("Question 1: How many steps are required to reach ZZZ?")
    print(f"Answer: {quiz_map.get_answer1()}")
    print(
        "Question 2: How many steps does it take before you're only on nodes"
        " that end with Z?"
    )
    print(f"Answer: {quiz_map.get_answer2()}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: How many steps are required to reach ZZZ?
# Answer: 18673
# Question 2: How many steps does it take before you're only on nodes that end with Z?
# Answer: 17972669116327
# Time elapsed: 0.08158349990844727 s

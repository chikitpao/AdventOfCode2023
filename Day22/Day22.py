""" Advent of Code 2023, Day 22
    Day 22: Sand Slabs
    Author: Chi-Kit Pao
"""

from collections import defaultdict
import copy
import os
import time


def debug(*args):
    if True:
        print(*args)


class Brick:
    def __init__(self, id_, start, end, fixed):
        self.id = id_
        self.start_xy = (start[0], start[1])
        self.start_z = start[2]
        self.end_xy = (end[0], end[1])
        self.end_z = end[2]
        self.fixed = fixed
        self.orientation = -1
        if self.start_z != self.end_z:
            self.orientation = 2
        else:
            for i in range(2):
                if self.start_xy[i] != self.end_xy[i]:
                    self.orientation = i
                    break
        # If still no orientation, then brick has size of one.
        # Just define orientation in z direction.
        if self.orientation == -1:
            self.orientation = 2

    def brick_pos_gen(self):
        for i in range(self.start_o(), self.end_o() + 1):
            pos = [self.start_xy[0], self.start_xy[1], self.start_z]
            pos[self.orientation] = i
            yield tuple(pos)

    def lower(self):
        self.start_z -= 1
        self.end_z -= 1

    def start_o(self):
        if self.orientation == 2:
            return self.start_z
        else:
            return self.start_xy[self.orientation]

    def end_o(self):
        if self.orientation == 2:
            return self.end_z
        else:
            return self.end_xy[self.orientation]

    def __repr__(self):
        return (
            f"Brick : {self.id} {self.start_xy} {self.start_z}"
            f" {self.end_xy} {self.end_z} {self.fixed} {self.orientation}"
        )

    def __str__(self):
        return self.__repr__()


def parse_input(lines):
    bricks = []
    min_values = [0, 0, 0]
    max_values = [0, 0, 0]

    def to_point(s):
        return tuple([int(s1) for s1 in s.split(",")])

    # Example inputs
    # 1,0,1~1,2,1
    for id, line in enumerate(lines, 1):
        s1, s2 = line.split("~")
        p1 = to_point(s1)
        p2 = to_point(s2)
        if p1 > p2:
            p1, p2 = p2, p1
        for i in range(3):
            min_values[i] = min(min_values[i], p1[i], p2[i])
            max_values[i] = max(max_values[i], p1[i], p2[i])
        assert all(map(lambda v: v >= 0, p1))
        assert all(map(lambda v: v >= 0, p2))
        # start, end, current lowest height, fixed
        bricks.append(Brick(id, p1, p2, p1[2] == 1))

    return bricks, min_values, max_values


def check_dropped_bricks(fixed_bricks, bricks):
    fixed_bricks_dict = defaultdict(list)
    fixed_bricks_count = 0
    for i in range(len(fixed_bricks)):
        for j in range(len(fixed_bricks[0])):
            for k in range(len(fixed_bricks[0][0])):
                if fixed_bricks[i][j][k] != 0:
                    fixed_bricks_dict[fixed_bricks[i][j][k]].append((j, k, i))
                    fixed_bricks_count += 1

    bricks_dict = defaultdict(list)
    bricks_count = 0
    for brick in bricks:
        for pos in brick.brick_pos_gen():
            bricks_dict[brick.id].append(pos)
            bricks_count += 1
    if fixed_bricks_count != bricks_count:
        debug(f"fixed_bricks_count {fixed_bricks_count} != bricks_count {bricks_count}")
        for k, v1 in bricks_dict.items():
            v2 = fixed_bricks_dict[k]
            if len(v1) != len(v2):
                debug(f"Difference {k}: {v1} {v2}")


def drop_bricks(bricks, min_values, max_values):
    assert all(map(lambda v: v == 0, min_values))

    def fix_brick(fixed_bricks, brick):
        for pos in brick.brick_pos_gen():
            fixed_bricks[pos[2]][pos[0]][pos[1]] = brick.id
            brick.fixed = True

    fixed_bricks = []
    for _ in range(max_values[2] + 1):
        z = []
        for x in range(max_values[0] + 1):
            x = [0] * (max_values[1] + 1)
            z.append(x)
        fixed_bricks.append(z)
    for brick in bricks:
        # fixed set on initialization but not glued in fixed_bricks
        if brick.fixed:
            fix_brick(fixed_bricks, brick)

    while True:
        handled = 0
        for height in range(1, max_values[2] + 1):
            for brick in bricks:
                if brick.fixed:
                    continue
                if brick.start_z == height:
                    if height == 1:
                        handled += 1
                        fix_brick(fixed_bricks, brick)
                    else:
                        if all(
                            map(
                                lambda pos: fixed_bricks[pos[2] - 1][pos[0]][pos[1]]
                                == 0,
                                brick.brick_pos_gen(),
                            )
                        ):
                            brick.lower()
                        else:
                            fix_brick(fixed_bricks, brick)
                        handled += 1
        if handled == 0:
            break

    check_dropped_bricks(fixed_bricks, bricks)

    return fixed_bricks


def part1(fixed_bricks, bricks):
    # Find bricks not safe for disintegration (-> only brick to support another)
    unsafe = set()
    for brick in bricks:
        supporting_bricks = set(
            [fixed_bricks[pos[2] - 1][pos[0]][pos[1]] for pos in brick.brick_pos_gen()]
        )
        supporting_bricks.discard(0)
        supporting_bricks.discard(brick.id)
        l = list(supporting_bricks)
        if len(l) == 1:
            unsafe.add(l[0])
    return len(bricks) - len(unsafe)

# Reuse Module from Day 20
class Module:
    def __init__(self, name, type_, outputs):
        self.name = name
        self.type = type_
        self.outputs = outputs
        # Flip-Flop: off or on
        # For Day 22: also for Conjunction
        self.state = False
        # Conjunction: {name: value}
        self.inputs = dict()
        # Common message queue
        self.queue = None

    def connect(self, other):
        if other.type == "&":
            other.inputs[self.name] = False

    def send(self, target, value):
        self.queue.append((self.name, target, value))
        if value:
            self.counters[1] += 1
        else:
            self.counters[0] += 1

    def react(self, source, value):
        if self.type == "":
            for o in self.outputs:
                self.send(o, value)
        elif self.type == "%":
            if value == False:
                self.state = not self.state
                for o in self.outputs:
                    self.send(o, self.state)
        elif self.type == "&":
            assert source in self.inputs
            self.inputs[source] = value
            # High wenn all values high, else low (different to Day 20)
            out_value = all(self.inputs.values())
            self.state = out_value
            for o in self.outputs:
                self.send(o, out_value)


def test_module(brick_id, modules_dict):
    counters = [0, 0]  # not really needed (only for Day 20)
    queue = []

    for d in modules_dict.values():
        d.queue = queue
        d.counters = counters
    try:
        start_module = modules_dict[str(brick_id)]
        start_module.type = ""
    except KeyError:
        return 0

    while(True):
        start_module.react("", True)
        while True:
            if len(queue) == 0:
                break
            signal = queue.pop(0)
            if signal[1] in modules_dict:
                modules_dict[signal[1]].react(signal[0], signal[2])
        if len(queue) == 0:
            break
    
    result = sum([m.state for m in modules_dict.values()])
    return result

def part2(fixed_bricks, bricks):
    supporting_bricks_dict = dict()
    supporting_bricks_set = set()
    supported_bricks = []
    supported_bricks_dict = defaultdict(list)
    for brick in bricks:
        supporting_bricks = set(
            [fixed_bricks[pos[2] - 1][pos[0]][pos[1]] for pos in brick.brick_pos_gen()]
        )
        supporting_bricks.discard(0)
        supporting_bricks.discard(brick.id)
        supporting_bricks_dict[brick.id] = supporting_bricks
        supporting_bricks_set.update(supporting_bricks)
        if len(supporting_bricks) > 0:
            supported_bricks.append(brick.id)
            for s in supporting_bricks:
                supported_bricks_dict[s].append(brick.id)

    new_set = supporting_bricks_set.union(supported_bricks)
    modules_dict = dict()
    for i in new_set:
        modules_dict[str(i)] = Module(str(i), "&", [])
    for k, v  in supported_bricks_dict.items():
        outputs = [str(i) for i in v]
        m = modules_dict[str(k)]
        m.outputs = outputs
        for o in m.outputs:
            m.connect(modules_dict[o])

    result = 0
    for i in supporting_bricks_set:
        result += test_module(i, copy.deepcopy(modules_dict))
    return result


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    bricks, min_values, max_values = parse_input(lines)
    fixed_bricks = drop_bricks(bricks, min_values, max_values)

    result1 = part1(fixed_bricks, bricks)
    print(
        "Question 1: Figure how the blocks will settle based on the snapshot.\n"
        " Once they've settled, consider disintegrating a single brick; how\n"
        " many bricks could be safely chosen as the one to get disintegrated?"
    )
    print(f"Answer: {result1}")

    result2 = part2(fixed_bricks, bricks)
    print(
        "Question 2: For each brick, determine how many other bricks would\n"
        " fall if that brick were disintegrated. What is the sum of the number\n"
        " of other bricks that would fall?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Figure how the blocks will settle based on the snapshot.
#  Once they've settled, consider disintegrating a single brick; how
#  many bricks could be safely chosen as the one to get disintegrated?
# Answer: 475
# Question 2: For each brick, determine how many other bricks would
#  fall if that brick were disintegrated. What is the sum of the number
#  of other bricks that would fall?
# Answer: 79144
# Time elapsed: 40.40147376060486 s

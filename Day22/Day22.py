""" Advent of Code 2023, Day 22
    Day 22: Sand Slabs
    Author: Chi-Kit Pao
"""

from collections import defaultdict
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
        return f"Brick : {self.id} {self.start_xy} {self.start_z}"\
            f" {self.end_xy} {self.end_z} {self.fixed} {self.orientation}"

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


def check_droped_bricks(fixed_bricks, bricks):
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

    check_droped_bricks(fixed_bricks, bricks)

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

    # result2 = 0
    # print(
    #    "Question 2: "
    # )
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Figure how the blocks will settle based on the snapshot.
#  Once they've settled, consider disintegrating a single brick; how
#  many bricks could be safely chosen as the one to get disintegrated?
# Answer: 475
# Time elapsed: 3.2847986221313477 s

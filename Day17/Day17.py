""" Advent of Code 2023, Day 17
    Day 17: Clumsy Crucible
    Author: Chi-Kit Pao
"""

from collections import defaultdict
import os
import time


class MapNode:
    UNVISITED = 0
    VISITING = 1
    VISITED = 2

    def __init__(self, row, col, prev_direction, dir_count, cost):
        self.row = row
        self.col = col
        self.prev_direction = prev_direction
        self.dir_count = dir_count
        self.neighbors = []
        self.own_cost = cost
        self.total_cost = None
        self.state = MapNode.UNVISITED

class Map:
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def __init__(self, lines):
        self.map = lines
        self.row_count = len(self.map)
        self.column_count = len(self.map[0])
        self.nodes = dict()
        self.nodes_pos = defaultdict(list)

    def calculate_heat_loss1(self):
        self.__init_map1()
        node1 = self.nodes[(0, 1, Map.EAST, 1)]
        node1.state = MapNode.VISITING
        node1.total_cost = node1.own_cost
        node2 = self.nodes[(1, 0, Map.SOUTH, 1)]
        node2.state = MapNode.VISITING
        node2.total_cost = node2.own_cost

        candidates = [node1, node2]
        while len(candidates) > 0:
            # process best candidate
            best_candidate = None
            for c in candidates:
                if best_candidate is None:
                    best_candidate = c
                else:
                    if c.total_cost < best_candidate.total_cost:
                        best_candidate = c

            if best_candidate.row == self.row_count - 1 and best_candidate.col == self.column_count - 1:
                return best_candidate.total_cost
            
            self.__process1(candidates, best_candidate)
            candidates.remove(best_candidate)
        return -1

    def valid_column(self, n):
        return 0 <= n < self.column_count

    def valid_row(self, n):
        return 0 <= n < self.row_count
    
    def __init_map1(self):
        self.nodes = dict()
        self.nodes_pos = defaultdict(list)
        
        for row in range(self.row_count):
            for col in range(self.column_count):
                for dir in range(4):
                    for dir_count in range(1, 4):
                        node = MapNode(row, col, dir, dir_count, ord(self.map[row][col]) - ord("0"))
                        self.nodes[(row, col, dir, dir_count)] = node
                        self.nodes_pos[(row, col)].append(node)
        for row in range(self.row_count):
            for col in range(self.column_count):
                for node_pos in self.nodes_pos[(row, col)]:
                    if self.valid_row(row - 1):
                        if node_pos.prev_direction == Map.NORTH:
                            self.nodes[(row, col, Map.NORTH, 1)].neighbors.append(self.nodes[(row - 1, col, Map.NORTH, 2)])
                            self.nodes[(row, col, Map.NORTH, 2)].neighbors.append(self.nodes[(row - 1, col, Map.NORTH, 3)])
                        elif node_pos.prev_direction != Map.SOUTH:
                            next_pos = self.nodes[(row - 1, col, Map.NORTH, 1)]
                            node_pos.neighbors.append(next_pos)
                    if self.valid_row(row + 1):
                        if node_pos.prev_direction == Map.SOUTH:
                            self.nodes[(row, col, Map.SOUTH, 1)].neighbors.append(self.nodes[(row + 1, col, Map.SOUTH, 2)])
                            self.nodes[(row, col, Map.SOUTH, 2)].neighbors.append(self.nodes[(row + 1, col, Map.SOUTH, 3)])
                        elif node_pos.prev_direction != Map.NORTH:
                            next_pos = self.nodes[(row + 1, col, Map.SOUTH, 1)]
                            node_pos.neighbors.append(next_pos)
                    if self.valid_column(col - 1):
                        if node_pos.prev_direction == Map.WEST:
                            self.nodes[(row, col, Map.WEST, 1)].neighbors.append(self.nodes[(row, col - 1, Map.WEST, 2)])
                            self.nodes[(row, col, Map.WEST, 2)].neighbors.append(self.nodes[(row, col - 1, Map.WEST, 3)])
                        elif node_pos.prev_direction != Map.EAST:
                            next_pos = self.nodes[(row, col - 1, Map.WEST, 1)]
                            node_pos.neighbors.append(next_pos)
                    if self.valid_column(col + 1):
                        if node_pos.prev_direction == Map.EAST:
                            self.nodes[(row, col, Map.EAST, 1)].neighbors.append(self.nodes[(row, col + 1, Map.EAST, 2)])
                            self.nodes[(row, col, Map.EAST, 2)].neighbors.append(self.nodes[(row, col + 1, Map.EAST, 3)])
                        elif node_pos.prev_direction != Map.WEST:
                            next_pos = self.nodes[(row, col + 1, Map.EAST, 1)]
                            node_pos.neighbors.append(next_pos)

    def __process1(self, candidates, node):
        assert (node.state == MapNode.VISITING)

        for other in node.neighbors:
            self.__visit1(candidates, node, other)
        node.state = MapNode.VISITED

    def __visit1(self, candidates, node, other):
        if other is None or other.state == MapNode.VISITED:
            return

        if other.state == MapNode.UNVISITED:
            other.total_cost = node.total_cost + other.own_cost
            other.state = MapNode.VISITING
            candidates.append(other)
        else:
            assert other.total_cost is not None
            temp_total_cost = node.total_cost + other.own_cost
            if temp_total_cost < other.total_cost:
                other.total_cost = temp_total_cost


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    map_ = Map(lines)

    result1 = map_.calculate_heat_loss1()
    print(
        "Question 1: Directing the crucible from the lava pool to the machine\n"
        " parts factory, but not moving more than three consecutive blocks in\n"
        " the same direction, what is the least heat loss it can incur?"
    )
    print(f"Answer: {result1}")

    # result2 = map_.calculate_heat_loss2()
    # print(
    #     "Question 2: Directing the ultra crucible from the lava pool to the\n"
    #     " machine parts factory, what is the least heat loss it can incur?"
    # )
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Directing the crucible from the lava pool to the machine
#  parts factory, but not moving more than three consecutive blocks in
#  the same direction, what is the least heat loss it can incur?
# Answer: 847
# Time elapsed: 28.42123770713806 s

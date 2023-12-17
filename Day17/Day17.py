""" Advent of Code 2023, Day 17
    Day 17: Clumsy Crucible
    Author: Chi-Kit Pao
"""

from collections import defaultdict
import functools
import os
import time

@functools.cache
def heuristic(row1, col1, row2, col2):
    return abs(row2 - row1) + abs(col2 - col1)

class MapNode:
    UNVISITED = 0
    VISITING = 1
    VISITED = 2

    def __init__(self, row, col, prev_direction, dir_count, cost):
        self.row = row
        self.col = col
        self.prev_direction = prev_direction
        self.dir_count = dir_count  # not used for part 2
        self.neighbors = []
        self.own_cost = cost
        self.total_cost = None
        self.state = MapNode.UNVISITED

    def __lt__(self, other):
        assert self.total_cost is not None and other.total_cost is not None
        return self.total_cost < other.total_cost

    def __eq__(self, other):
        assert self.total_cost is not None and other.total_cost is not None
        return self.total_cost == other.total_cost

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
            candidates.sort(key=lambda c: c.total_cost)
            best_candidate = candidates.pop(0)

            if best_candidate.row == self.row_count - 1 and best_candidate.col == self.column_count - 1:
                return best_candidate.total_cost
            
            self.__process1(candidates, best_candidate)
        return -1
    
    def calculate_heat_loss2(self):
        self.__init_map2()
        candidates = []
        for i in range(4, 11):
            node1 = self.nodes[(0, i, Map.EAST, -1)]
            node1.state = MapNode.VISITING
            node1.total_cost = self.edge_cost2(0, 0, 0, i)
            node2 = self.nodes[(i, 0, Map.SOUTH, -1)]
            node2.state = MapNode.VISITING
            node2.total_cost = self.edge_cost2(0, 0, i, 0)
            candidates.append(node1)
            candidates.append(node2)

        while len(candidates) > 0:
            # process best candidate
            candidates.sort(key=lambda c: (c.total_cost + heuristic(c.row, c.col, self.row_count - 1, self.column_count - 1)))
            best_candidate = candidates.pop(0)

            if best_candidate.row == self.row_count - 1 and best_candidate.col == self.column_count - 1:
                return best_candidate.total_cost
            
            self.__process2(candidates, best_candidate)
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

    def __init_map2(self):
        # REMARK: no intermediate nodes for question 2 (i.e. no north 1 to north 2 to north 3 etc.)
        self.nodes = dict()
        self.nodes_pos = defaultdict(list)
        
        for row in range(self.row_count):
            for col in range(self.column_count):
                for dir in range(4):
                    node = MapNode(row, col, dir, -1, ord(self.map[row][col]) - ord("0"))
                    self.nodes[(row, col, dir, -1)] = node
                    self.nodes_pos[(row, col)].append(node)
        for row in range(self.row_count):
            for col in range(self.column_count):
                for node_pos in self.nodes_pos[(row, col)]:
                    for i in range(4, 11):
                        if node_pos.prev_direction in (Map.NORTH, Map.SOUTH):
                            if self.valid_column(col - i):
                                node_pos.neighbors.append(self.nodes[(row, col - i, Map.WEST, -1)])
                            if self.valid_column(col + i):
                                node_pos.neighbors.append(self.nodes[(row, col + i, Map.EAST, -1)])
                        else:
                            if self.valid_column(row - i):
                                node_pos.neighbors.append(self.nodes[(row - i, col, Map.NORTH, -1)])
                            if self.valid_column(row + i):
                                node_pos.neighbors.append(self.nodes[(row + i, col, Map.SOUTH, -1)])

    def __process2(self, candidates, node):
        assert (node.state == MapNode.VISITING)

        for other in node.neighbors:
            self.__visit2(candidates, node, other)
        node.state = MapNode.VISITED

    def __visit2(self, candidates, node, other):
        if other is None or other.state == MapNode.VISITED:
            return

        new_total_cost = node.total_cost + self.edge_cost2(node.row, node.col, other.row, other.col)
        if other.state == MapNode.UNVISITED:
            other.total_cost = new_total_cost
            other.state = MapNode.VISITING
            candidates.append(other)
        else:
            assert other.total_cost is not None
            if new_total_cost < other.total_cost:
                other.total_cost = new_total_cost
    
    def edge_cost2(self, row1, col1, row2, col2):
        total_cost = 0
        if row1 == row2:
            if col1 < col2:
                for j in range(col1 + 1, col2 + 1):
                    total_cost += ord(self.map[row1][j]) - ord("0")
            else:
                for j in range(col1 - 1, col2 - 1, -1):
                    total_cost += ord(self.map[row1][j]) - ord("0")
        elif col1 == col2:
            if row1 < row2:
                for i in range(row1 + 1, row2 + 1):
                    total_cost += ord(self.map[i][col1]) - ord("0")
            else:
                for i in range(row1 - 1, row2 - 1, -1):
                    total_cost += ord(self.map[i][col1]) - ord("0")
        else:
            raise RuntimeError("Invalid neighbors!")
        return total_cost


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    map_ = Map(lines)

    start_time1 = time.time()
    result1 = map_.calculate_heat_loss1()
    print(
        "Question 1: Directing the crucible from the lava pool to the machine\n"
        " parts factory, but not moving more than three consecutive blocks in\n"
        " the same direction, what is the least heat loss it can incur?"
    )
    print(f"Answer: {result1}")
    print(f"Time elapsed (part 1): {time.time() - start_time1} s")

    result2 = map_.calculate_heat_loss2()
    print(
        "Question 2: Directing the ultra crucible from the lava pool to the\n"
        " machine parts factory, what is the least heat loss it can incur?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Directing the crucible from the lava pool to the machine
#  parts factory, but not moving more than three consecutive blocks in
#  the same direction, what is the least heat loss it can incur?
# Answer: 847
# Time elapsed (part 1): 26.386030197143555 s
# Question 2: Directing the ultra crucible from the lava pool to the
#  machine parts factory, what is the least heat loss it can incur?
# Answer: 997
# Time elapsed: 103.82118701934814 s

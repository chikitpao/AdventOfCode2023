""" Advent of Code 2023, Day 23
    Day 23: A Long Walk
    Author: Chi-Kit Pao
    REMARK: Requires MatPlotLib, NetworkX and Numpy to run this program.
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os
import time


def debug(*args):
    if True:
        print(*args)

class Junction:
    def __init__(self, id_, pos, neighbors):
        self.id = id_
        self.pos = pos
        # Neighbor tiles
        self.neighbors = neighbors
        # Neighbor Junctions
        self.junction_ids = []

class Edge:
    def __init__(self, node1, node2, distance):
        self.node1 = node1
        self.node2 = node2
        self.distance = distance

    def __repr__(self):
        return f"Edge(node1={self.node1}, node2={self.node2}, distance={self.distance})"
    

class Map:
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    EMPTY = "."
    OCCUPIED = "#"
    SLOPE_TILES = [">", "v", "<", "^"]

    def __init__(self, lines, consider_slopes):
        self.map = lines
        self.column_count = len(lines[0])
        self.row_count = len(lines)
        self.start_pos = (0, 1)
        assert self.map[self.row_count - 1][self.row_count - 2] == Map.EMPTY
        self.end_pos = (self.row_count - 1, self.row_count - 2)
        self.junctions = []
        self.junctions_dict = dict()
        self.longest_path_length = None
        self.consider_slopes = consider_slopes

        def add_junction(junction):
            self.junctions.append(junction)
            self.junctions_dict[junction.pos] = junction

        start = Junction(len(self.junctions), self.start_pos, self.get_neighbors(self.start_pos, False))
        self.start_junction_id = start.id
        add_junction(start)
        end = Junction(len(self.junctions), self.end_pos, self.get_neighbors(self.start_pos, False))
        self.end_junction_id = end.id
        add_junction(end)
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.map[row][col] == Map.OCCUPIED:
                    continue
                pos = (row, col)
                neighbors = self.get_neighbors(pos, False)
                if neighbors.count(None) <= 1:
                    assert self.map[row][col] == Map.EMPTY
                    add_junction(Junction(len(self.junctions), pos, neighbors))
        
        self.connections = dict()
        for junction in self.junctions:
            if junction.pos == self.end_pos:
                continue
            for dir in range(4):
                edge = self.trace_connection(junction, dir)
                if edge is not None:
                    self.connections[edge.node1, edge.node2] = edge
                    junction.junction_ids.append(edge.node2)
        self.build_graph()

    def build_graph(self):
        # Build graph
        graph = nx.DiGraph()
        graph.add_nodes_from([junction.pos for junction in self.junctions])
        for edge in self.connections.values():
            graph.add_edge(self.junctions[edge.node1].pos, self.junctions[edge.node2].pos, weight=edge.distance)
        
        # Set node position
        pos = dict()
        nodes = set(graph)
        for node in nodes:
            pos[node] = np.array([node[1], node[0]])
        nx.draw(graph, pos=pos, with_labels=True)
        # nx.draw_networkx_edge_labels(graph, pos)
        ax = plt.gca()
        ax.set_axis_off()
        # Uncomment this line to show the graph.
        # plt.show()

        try:
            longest_path = nx.dag_longest_path(graph)
            self.longest_path_length = nx.dag_longest_path_length(graph)
            # Output: [(0, 1), (13, 5), (11, 43), (15, 53), (7, 85), (5, 103), (35, 103), (33, 127), (67, 127), (83, 125), (103, 129), (131, 137), (140, 139)]
            debug("longest_path", longest_path)
        except nx.exception.NetworkXUnfeasible:
            # Handle exception for Part 2:
            # networkx.exception.NetworkXUnfeasible: Graph contains a cycle or graph changed during iteration
            pass

    def get_neighbor(self, pos, dir, check_slope):
        offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        new_pos = (pos[0] + offsets[dir][0], pos[1] + offsets[dir][1])
        if new_pos[0] < 0 or new_pos[0] >= self.row_count:
            return None
        if new_pos[1] < 0 or new_pos[1] >= self.column_count:
            return None
        new_tile = self.map[new_pos[0]][new_pos[1]]
        if new_tile == Map.OCCUPIED:
            return None
        if check_slope:
            current_tile = self.map[pos[0]][pos[1]]
            if current_tile != Map.EMPTY and Map.SLOPE_TILES[dir] != current_tile:
                return None
        return new_pos
    
    def get_neighbors(self, pos, check_slope):
        return [self.get_neighbor(pos, dir, check_slope) for dir in range(4)]
    
    def trace_connection(self, junction, dir):
        distance = 0
        consider_slopes = self.consider_slopes
        current_pos = self.get_neighbor(junction.pos, dir, consider_slopes)
        if current_pos is None:
            return None
        distance += 1
        opposite_direction = {Map.EAST: Map.WEST, Map.SOUTH: Map.NORTH, 
                              Map.WEST: Map.EAST, Map.NORTH: Map.SOUTH}
        last_dir = dir
        while current_pos not in self.junctions_dict:
            found_next = False
            for d in range(4):
                if d == opposite_direction[last_dir]:
                    continue
                next_pos = self.get_neighbor(current_pos, d, consider_slopes)
                if next_pos is None:
                    continue
                found_next = True
                distance += 1
                current_pos = next_pos
                last_dir = d
                break
            if not found_next:
                return None
            
        next_junction = self.junctions_dict[current_pos]
        return Edge(junction.id, next_junction.id, distance)


# [total distance, list with junction IDs]
current_longest_path = None

def find_longest_path_dfs(map_, junction, path):
    """ Recursive function to find the longest path using Depth-first search.
    """
    global current_longest_path

    # junction before end
    if map_.end_junction_id in junction.junction_ids:
        path.append(map_.end_junction_id)
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += map_.connections[(path[i], path[i+1])].distance
        if current_longest_path is None or current_longest_path[0] < total_distance:
            current_longest_path = [total_distance, path.copy()]
        path.pop(-1)
        return

    for id_ in junction.junction_ids:
        if id_ in path:
            continue
        path.append(id_)
        find_longest_path_dfs(map_, map_.junctions[id_], path)
        path.pop(-1)


def main():
    start_time = time.time()

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    map_ = Map(lines, True)

    print(
        "Question 1: Find the longest hike you can take through the hiking\n"
        " trails listed on your map. How many steps long is the longest hike?"
    )
    print(f"Answer: {map_.longest_path_length}")

    map_ = Map(lines, False)
    find_longest_path_dfs(map_, map_.junctions[map_.start_junction_id], 
                                    [map_.start_junction_id])
    global current_longest_path
    result2 = current_longest_path[0]
    # Output:
    # Longest path: [(0, 1), (13, 5), (11, 43), (15, 53), (7, 85), (33, 85), 
    #  (53, 79), (57, 109), (35, 103), (5, 103), (33, 127), (67, 127), 
    #  (83, 125), (103, 129), (113, 99), (79, 107), (81, 75), (75, 61), 
    #  (111, 65), (103, 35), (87, 39), (63, 29), (63, 53), (37, 59), (39, 31), 
    #  (43, 5), (59, 13), (89, 13), (105, 15), (123, 33), (133, 61), (123, 79), 
    #  (127, 103), (131, 137), (140, 139)]
    debug("Longest path:", [map_.junctions[id_].pos for id_ in current_longest_path[1]])
    print(
        "Question 2: Find the longest hike you can take through the\n"
        " surprisingly dry hiking trails listed on your map. How many steps\n"
        " long is the longest hike?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Find the longest hike you can take through the hiking
#  trails listed on your map. How many steps long is the longest hike?
# Answer: 2206
# Question 2: Find the longest hike you can take through the
#  surprisingly dry hiking trails listed on your map. How many steps
#  long is the longest hike?
# Answer: 6490
# Time elapsed: 20.89226746559143 s

""" Advent of Code 2023, Day 25
    Day 25: Snowverload
    Author: Chi-Kit Pao
    REMARK: Requires MatPlotLib and NetworkX to run this program.
"""

import matplotlib.pyplot as plt
import networkx as nx
import os
import time


def debug(*args):
    if True:
        print(*args)


def main():
    start_time = time.time()

    edges = []

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
        for line in lines:
            start, p2 = line.split(":")
            p2_list = p2.split()
            for end in p2_list:
                edges.append((start, end))

    # Build graph
    graph = nx.Graph()
    for edge in edges:
        graph.add_edge(edge[0], edge[1])

    # REMARK: Showed graph and stored it as "AoC2023Day25_Graph_before.png".
    # Figured out that these three edges shall be removed:
    # REMARK: Afterwards showed graph again and stored it as "AoC2023Day25_Graph_after.png".
    graph.remove_edge("txf", "xnn")
    graph.remove_edge("jjn", "nhg")
    graph.remove_edge("lms", "tmc")

    nx.draw(graph, with_labels=True, node_color="blue")
    ax = plt.gca()
    ax.set_axis_off()
    plt.show()
    # plt.savefig(os.path.join(os.path.dirname(__file__), "test.png"))

    result1 = len(nx.node_connected_component(graph, "gdd")) * len(nx.node_connected_component(graph, "qgn"))
    print(
        "Question: Find the three wires you need to disconnect in order to\n"
        " divide the components into two separate groups. What do you get if\n"
        " you multiply the sizes of these two groups together?"
    )
    print(f"Answer: {result1}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question: Find the three wires you need to disconnect in order to
#  divide the components into two separate groups. What do you get if
#  you multiply the sizes of these two groups together?
# Answer: 562912
# Time elapsed: 10.368342161178589 s

import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)


import networkx as nx
import matplotlib.pyplot as plt


# Defining a Class
class GraphVisualization:
    def __init__(self):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


G = GraphVisualization()


def prep():
    nodes = {}
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    for line in lines:
        node, connections = line.split(":")
        connections = connections.split()

        if node in nodes.keys():
            nodes[node].extend(connections)
        else:
            nodes[node] = connections

        for c in connections:
            G.addEdge(node, c)

            if c in nodes.keys():
                nodes[c].append(node)
            else:
                nodes[c] = [node]
    return nodes


def remove_edge(nodes, a, b):
    nodes[a].remove(b)
    nodes[b].remove(a)


def size_graph(nodes, start):
    visited = set()
    Q = [start]
    while Q:
        curr = Q.pop()
        visited.add(curr)
        for c in nodes[curr]:
            if c not in visited:
                Q.append(c)

    return len(visited)


def part1(nodes):
    remove_edge(nodes, "xmv", "dht")
    remove_edge(nodes, "cms", "thk")
    remove_edge(nodes, "rcn", "xkf")
    print("Part 1: ", size_graph(nodes, "xmv") * size_graph(nodes, "dht"))


def part2(lines):
    for line in lines:
        pass

    print(
        "Part 2: ",
    )


part1(prep())
print()
part2(prep())

G.visualize()

import fileinput, bisect
import functools
import os
import sys
import heapq

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from navigation import north, south, east, west, in_bounds
from util import get_input_file, timer_func as timer, print_grid, BFS_search

filename = get_input_file(sys.argv[1:], script_dir)


class Node:
    def __init__(self, length, point, path=[]):
        self.length = length
        self.point = point
        self.path = tuple(path)

    def __repr__(self):
        return f"Node value: {self.length}"

    def __lt__(self, other):
        return other.length < self.length

    def __hash__(self):
        return hash((self.length, self.point, self.path))

    def __eq__(self, other: object) -> bool:
        self.length == other.length and self.point == other.point and self.path == other.path


def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    grid = []
    trees = []
    slopes = []
    ymax = len(lines)
    xmax = len(lines[0])

    for i, y in enumerate(lines):
        grid.append([])
        for j, x in enumerate(y):
            p = (j, i)
            if i == 0:
                if x == ".":
                    start = p
            if x == "#":
                trees.append(p)
            elif x != ".":
                slopes.append((p, x))
            grid[i].append(x)
    return start, grid, (xmax, ymax), trees, slopes


dirs = [north, east, south, west]
slope_dirs = ["^", ">", "v", "<"]


def get_slope_dir(char):
    return dirs[slope_dirs.index(char)]


def is_slope(p, grid):
    x, y = p
    return grid[y][x] in slope_dirs


def is_path(p, grid):
    x, y = p
    return grid[y][x] != "#"


def find_path(grid, start, maxes):
    start = (Node(0, start), [])
    paths = []
    visited = {}
    Q = []
    heapq.heappush(Q, start)
    while Q:
        curr = heapq.heappop(Q)
        length = curr[0].length
        pcurr = curr[0].point
        if pcurr in visited:
            if length > visited[pcurr]:
                visited[pcurr] = length
            else:
                continue
        else:
            visited[pcurr] = length
        if is_slope(pcurr, grid):
            d = get_slope_dir(grid[pcurr[1]][pcurr[0]])
            new_p = d(pcurr)
            heapq.heappush(Q, (Node(length + 1, new_p), curr[1] + [pcurr]))
        else:
            cannot_move = True
            for a in dirs:
                new_p = a(pcurr)
                if (
                    in_bounds(new_p, maxes)
                    and is_path(new_p, grid)
                    and not new_p in curr[1]
                ):
                    if is_slope(new_p, grid):
                        d = get_slope_dir(grid[new_p[1]][new_p[0]])
                        if dirs[dirs.index(d) - 2] == a:
                            continue
                    cannot_move = False
                    heapq.heappush(Q, (Node(length + 1, new_p), curr[1] + [pcurr]))
            if cannot_move:
                paths.append(curr)
    return paths


class Intersection:
    def __init__(self, point, edges=[]):
        self.point = point
        self.edges = edges

    def __repr__(self):
        return f"Point: {self.point}, Edges: {self.edges}"

    def __lt__(self, other):
        return other.point < self.point


class MapNode:
    def __init__(self, point, children):
        self.point = point
        self.children = children
        self.is_intersection = len(children) > 2

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"Point: {self.point}, Children: {self.children}"


@timer
def buildGraph(grid, maxes):
    points = {}
    visited = set()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            point = (x, y)
            if is_path(point, grid):
                children = list(
                    filter(
                        lambda new_p: in_bounds(new_p, maxes)
                        and is_path(new_p, grid)
                        and not new_p in visited,
                        [a(point) for a in dirs],
                    )
                )
                points[point] = MapNode(point, children)
    return points


@timer
def makeLegs(points, grid, start, end):
    intersections = {}
    for node in points.values():
        if node.is_intersection:
            edges = []
            for child in node.children:
                # follow child and count path
                currNode = points[child]
                path = [node.point]
                count = 1
                while not currNode.is_intersection:
                    count += 1
                    path.append(currNode.point)
                    children = list(filter(lambda x: not x in path, currNode.children))
                    if not children:
                        intersections[currNode.point] = Intersection(
                            currNode.point, [(node.point, len(path) - 1, count)]
                        )
                        break
                        # reached a start or end
                    else:
                        currNode = points[children[0]]
                edge = currNode.point, len(path), count
                edges.append(edge)
            intersections[node.point] = Intersection(node.point, edges)
    return intersections


@timer
def find_path_map_generic(intersections, start, maxes):
    return BFS_search(
        [start],
        getHeapItem=lambda point: intersections[point[0]],
        end_condition=lambda intersection: intersection.point[1] == maxes[1] - 1,
        returner=lambda intersection, weight, visited: (weight, visited),
        getChildren=lambda intersection: intersection.edges,
        getVisitor=lambda edge: edge[0],
        getWeight=lambda edge: edge[1],
    )


@timer
def find_path_map(intersections, start, maxes):
    start = (0, [], intersections[start])
    paths = []
    Q = []
    heapq.heappush(Q, start)
    while Q:
        curr = heapq.heappop(Q)
        old_point = curr[2].point

        length = curr[0]
        path = curr[1]
        if old_point[1] == maxes[1] - 1:
            paths.append((length, path))
        for edge in curr[2].edges:
            new_point = edge[0]
            if new_point in path:
                continue
            else:
                newIntersection = intersections[new_point]
                heapq.heappush(
                    Q, (length + edge[1], path + [new_point], newIntersection)
                )
    return paths


def part1(start, grid, maxes, trees, slopes):
    paths = find_path(grid, start, maxes)
    paths.sort(key=lambda x: x[0], reverse=True)
    # print_grid((0, 0), maxes, ".", [("O", paths[0][1])])
    print("Part 1: ", paths[0][0].length)


def part2(start, grid, maxes, trees, slopes):
    points = buildGraph(grid, maxes)
    intersections = makeLegs(points, grid, start, trees)
    # print(points)
    # print(intersections.keys())
    paths2 = find_path_map_generic(intersections, start, maxes)
    paths = find_path_map(intersections, start, maxes)
    if paths == paths2:
        print("TRUE")
    paths2.sort(key=lambda x: x[0], reverse=True)
    print(paths2[0][0] - 1)
    # print(paths)
    print("Part 2: ", paths2[0][0] - 1)


# part1(*prep())
print()
part2(*prep())

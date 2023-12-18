import fileinput, bisect
import functools
import os
import sys
import heapq
import numpy as np

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from navigation import north, east, south, west
from util import get_input_file, timer_func as timer, print_grid

filename = get_input_file(sys.argv[1:], script_dir)


def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    digs = []
    for l in lines:
        d, depth, color = l.split()
        depth = int(depth)
        color = color[1:-1]
        digs.append((d, depth, color))
    return digs


dirs = {"R": east, "D": south, "L": west, "U": north}

hexa_dirs = {"0": "R", "1": "D", "2": "L", "3": "U"}


def touches_outside(location, outside):
    x, y = location
    return (
        (x, y - 1) in outside
        or (x + 1, y) in outside
        or (x, y + 1) in outside
        or (x - 1, y) in outside
    )


def get_adjecents(point, mins, maxes, fil=lambda x: True):
    x, y = point
    adjacents = []
    xmax, ymax = maxes
    xmin, ymin = mins
    if (x + 1) < xmax:
        adjacents.append((x + 1, y))
    if (y + 1) < ymax:
        adjacents.append((x, y + 1))
    if (x - 1) >= xmin:
        adjacents.append((x - 1, y))
    if (y - 1) >= ymin:
        adjacents.append((x, y - 1))
    return adjacents


def is_inside(location, outline):
    return location not in outline


@timer
def floodfill(point, outline, fill, mins, maxes):
    Q = [point]
    while Q:
        point = Q.pop()
        fill.add(point)
        for a in get_adjecents(point, mins, maxes):
            if not a in fill:
                if is_inside(a, outline):
                    Q.append(a)


def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


@timer
def part1(digs):
    max_x = 0
    max_y = 0
    point = (0, 0)
    outline = set()
    outline.add(point)
    xs = []
    ys = []

    for dig in digs:
        d, depth, color = dig
        d = dirs[d]
        for i in range(depth):
            point = d(point)
            outline.add(point)
        xs.append(point[0])
        ys.append(point[1])

    # shoelace formula
    A = PolyArea(xs, ys)

    # picks theorem https://en.wikipedia.org/wiki/Pick's_theorem
    interior = int(A + 1 - (len(outline) // 2))
    total = interior + len(outline)
    min_x = min([p[0] for p in outline])
    min_y = min([p[1] for p in outline])
    mi = (min_x, min_y)
    max_x = max([p[0] for p in outline]) + 1
    max_y = max([p[1] for p in outline]) + 1
    ma = (max_x, max_y)
    fill = set()
    start = (1, 1)
    floodfill(start, outline, fill, mi, ma)
    # for y in range(min_y, max_y):
    #     for x in range(min_x, max_x):
    #         find_location((x,y), outside, outline, ma)
    # print_grid(mi, (max_x, max_y), ".", [("#", outline), ("#", fill)])
    print("Part 1: ", len(outline) + len(fill), total)

# stolen from someone else.
def shoelace_area(points):
    n = len(points)
    res = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        res += x1 * y2 - x2 * y1
    return abs(res) >> 1


@timer
def part2(digs):
    outline = []
    point = (0, 0)
    boundary = 0
    xs = []
    ys = []
    for dig in digs:
        d, depth, color = dig
        dmap = color[-1]

        depth = int(color[1:-1], 16)
        d = dirs[hexa_dirs[dmap]]
        boundary += depth
        point = d(point, depth)
        outline.append(point)
        xs.append(point[0])
        ys.append(point[1])

    print("calculated")
    print(boundary, len(outline))
    # shoelace formula
    A = PolyArea(xs, ys)
    print(A)
    A2 = shoelace_area(outline)
    print("A2", A2)

    # picks theorem https://en.wikipedia.org/wiki/Pick's_theorem
    interior = A2 + 1 - boundary // 2
    print(interior, boundary)
    total = interior + boundary
    print(
        "Part 2: ",
        total,
    )


part1(prep())
print()
part2(prep())

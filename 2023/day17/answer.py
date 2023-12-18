import fileinput, bisect
import functools
import os
import sys
import queue
import heapq  # min heap

P = complex

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from navigation import north, south, east, west, in_bounds
from util import get_input_file, timer_func as timer, print_grid

filename = get_input_file(sys.argv[1:], script_dir)


def prep():
    points = {}
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    max_x = len(lines[0])
    max_y = len(lines)

    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            point = (x, y)
            heat_loss = int(c)
            points[point] = heat_loss
    return points, (max_x, max_y)


paths = queue.PriorityQueue()
visited = {}
dirs = {
    north: [north, east, west],
    south: [south, east, west],
    east: [south, east, north],
    west: [south, west, north],
}


def get_heat_loss(p_chain, grid):
    return sum([grid[p] for p in p_chain])


def get_function(name):
    return globals()[name]


class State:
    def __init__(self, loss, p, d, c):
        self.loss = loss
        self.p = p
        self.d = d
        self.c = c
        self.key = (self.p, self.d, self.c)

    def __lt__(self, other):
        return (self.loss, self.c) < (other.loss, other.c)


@timer
def main():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    max_x = len(lines[0])
    max_y = len(lines)
    grid = {}
    for y, r in enumerate(lines):
        for x, v in enumerate(r):
            grid[P(x, y)] = int(v)
    end = P(max_x - 1, max_y - 1)

    def solve(part1):
        seen = set()
        Q = [State(0, 0, 1, 0), State(0, 0, 1j, 0)]
        while Q:
            s = heapq.heappop(Q)
            if s.key in seen:
                continue
            seen.add(s.key)
            loss, p, d, c = s.loss, s.p, s.d, s.c

            if p == end and (part1 or c >= 4):
                return loss
            # if p not in grid:
            # 	continue
            if ((part1 and c < 3) or (not part1 and c < 10)) and p + d in grid:
                heapq.heappush(Q, State(loss + grid[p + d], p + d, d, c + 1))

            d *= 1j
            if (part1 or 4 <= c) and p + d in grid:
                heapq.heappush(Q, State(loss + grid[p + d], p + d, d, 1))
            d *= -1
            if (part1 or 4 <= c) and p + d in grid:
                heapq.heappush(Q, State(loss + grid[p + d], p + d, d, 1))

    return solve(True), solve(False)


@timer
def find_path(maxes, grid, goal, min=0, max=3):
    seen = set()
    Q = [(0, (0, east.__name__), (0, 0))]
    ps = []
    while Q:
        loss, dir_info, path = heapq.heappop(Q)
        location = path
        d_count, dir_name = dir_info
        dir = get_function(dir_name)
        key = (location, dir_name, d_count)
        if key in seen:
            continue
        seen.add(key)
        # print_grid((0,0), maxes, '.', [('#', path), ('@', [path[-1]])])
        if location == goal and d_count > min:
            return loss, path
        else:
            for d in dirs[dir]:
                new_p = d(location)
                if in_bounds(new_p, maxes):
                    new_loss = loss + grid[new_p]
                    if d == dir:
                        if d_count < max:
                            new_count = d_count + 1
                            heapq.heappush(
                                Q, (new_loss, (new_count, d.__name__), new_p)
                            )
                    else:
                        if d_count > min:
                            new_count = 1
                            heapq.heappush(
                                Q, (new_loss, (new_count, d.__name__), new_p)
                            )
    return ps


def part1(points, maxes):
    goal = (maxes[0] - 1, maxes[1] - 1)
    loss, path = find_path(maxes, points, goal)
    # print_grid((0, 0), maxes, ".", [("#", path), ("@", [path[-1]])])
    print("Part 1: ", loss)


def part2(points, maxes):
    goal = (maxes[0] - 1, maxes[1] - 1)
    loss, path = find_path(maxes, points, goal, 3, 10)

    print(
        "Part 2: ", loss
    )


print(main())
part1(*prep())
print()
part2(*prep())

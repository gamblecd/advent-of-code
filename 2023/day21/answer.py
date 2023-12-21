import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))
from navigation import north, east, south, west, in_bounds
from util import get_input_file, timer_func as timer, print_grid

filename = get_input_file(sys.argv[1:], script_dir)


def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    grid = []
    start = (0, 0)
    for y, line in enumerate(lines):
        grid.append([])
        for x, char in enumerate(line):
            grid[y].append(char)
            if char == "S":
                start = (x, y)
        grid[y] = tuple(grid[y])
    grid = tuple(grid)
    return start, grid


def is_garden(grid, point):
    (x, y) = point
    x = x % len(grid[0])
    y = y % len(grid)

    return grid[y][x] == "." or grid[y][x] == "S"


def is_start(grid, point):
    (x, y) = point
    x = x % len(grid[0])
    y = y % len(grid)

    return grid[y][x] == "S"


dirs = [north, south, east, west]


@functools.lru_cache(maxsize=None)
def take_n_steps_n_points(grid, points, steps):
    new_points = set()
    for _ in range(steps):
        for p in points:
            new_points.update(take_n_steps(grid, p, steps))
    return new_points


@functools.lru_cache(maxsize=None)
def take_n_steps(grid, point, steps):
    points = set()
    points.add(point)
    for _ in range(steps):
        points = take_step(grid, points)
    return points


@functools.lru_cache(maxsize=None)
def take_point_step(grid, point):
    new_points = set()
    for d in dirs:
        np = d(point)
        if is_garden(grid, np):
            new_points.add(np)
    return new_points


def take_step(grid, points, step=0):
    maxes = (len(grid[0]), len(grid))
    new_points = set()
    for p in points:
        new_points.update(take_point_step(tuple(grid), p))
        # if (is_start(grid, np)):
        #     print(step)
    return new_points


def part1(start, grid):
    steps = 6
    starts = set()
    starts.add(start)
    for _ in range(steps):
        starts = take_step(grid, starts)

    # print_grid((0, 0), (len(grid[0]), len(grid)), ".", [("O", starts)])
    print("Part 1: ", len(starts))


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i : i + n]


def take_steps(grid, starts, steps):
    for _ in range(steps):
        new_starts = set()
        for p in starts:
            new_starts.update(take_n_steps(grid, p, 1))
        starts = new_starts
    return len(starts)


@timer
def part2(start, grid):
    steps = start[0]
    starts = set()
    starts.add(start)
    a0 = take_steps(grid, starts, steps)
    print(steps, a0)
    y = len(grid)
    steps += y
    a1 = take_steps(grid, starts, steps)
    print(steps, a1)

    steps += y
    a2 = take_steps(grid, starts, steps)
    print(steps, a2)

    print("Part 2: ", len(starts))


def ftest(n):
    return 13 + 25 * n + 91 * (n**2)


# inputted (0, 1, 2), a0, a1, a2 from above to compe up with quadratic formula.
def f(n): #https://www.wolframalpha.com/input?i=quadratic+%280%2C+13%29+%281%2C+129%29+%282%2C427%29+
    return 3648 + 14604 * n + 14529 * (n**2)


print(ftest((500-5)//11))
print(f(202300))


part1(*prep())
print()
part2(*prep())

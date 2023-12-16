import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))
from navigation import north, south, east, west, in_bounds
from util import get_input_file, timer_func as timer, print_grid

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    grid = []
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    for y, row in enumerate(lines):
        grid.append([])
        for x in row:
            grid[y].append(x)
            
    return grid

def gp(grid, point):
    return grid[point[1]][point[0]]

def traverse_stack(grid, point, direction):
    curr = gp(grid, point)
    if (curr == '|'):
        if direction == east or direction == west:
            return [north, south]
    if (curr == '-'):
        if direction == north or direction == south:
            return [east, west]
    elif (curr == '\\'):
        if (direction == north):
            direction = west;
        elif direction == south:
            direction = east
        elif direction == east:
            direction = south
        elif direction == west:
            direction = north
    elif (curr == '/'):
        if (direction == north):
            direction = east;
        elif direction == south:
            direction = west
        elif direction == east:
            direction = north
        elif direction == west:
            direction = south
    return [direction]

def energy_max(grid, starting_location, starting_dir, maxes):
    paths = [(starting_location, starting_dir)]
    visited = set()
    while len(paths) > 0:
        loc, dir = paths.pop()
        visited.add((loc, dir))
        directions = traverse_stack(grid, loc, dir)
        for d in directions:
            p = d(loc)
            if in_bounds(p, maxes) and not (p, d) in visited:
                paths.append((p, d))
    #traverse(grid, starting_location, starting_dir)
    energized  = set(x[0] for x in visited)
    return len(energized)

def part1(grid):
    maxes = (len(grid[0]), len(grid))
    starting_dir = east
    starting_location = (0,0)
    print("Part 1: ",energy_max(grid, starting_location, starting_dir, maxes))

def part2(grid):
    maxes = (len(grid[0]), len(grid))
    starts = []
    #North
    for i in range(len(grid)):
        starts.append(((i,0),south))
    #south
    for i in  range(len(grid)):
        starts.append(((i, len(grid)-1),south))
    #west
    for i in range(len(grid[0])):
        starts.append(((0,i),east))
    #east
    for i in range(len(grid[0])):
        starts.append(((len(grid)-1, i),west))
    print("Part 2: ",max([energy_max(grid, loc, dir, maxes) for loc, dir in starts]))

part1(prep())
print()
part2(prep())
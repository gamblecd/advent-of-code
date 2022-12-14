import fileinput, bisect
import functools
import os
import sys
import json

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

rock_paths = []
edges = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    points = [[int(p) for p in point.strip().split(",")]
              for point in line_data.split("->")]
    rock_paths.append(points)
    edges.append(points[0])
    edges.append(points[-1])

rocks = set()
sand = set()
falling_path = set();
def enum_rocks():
    for path in rock_paths:
        for i, point in enumerate(path):
            x = point[0]
            y = point[1]
            rocks.add((x,y))
            if i != len(path)-1:  # If we aren't at the end connect the dots
                next_point = path[i+1]
                for j in range(next_point[0], x):
                    rocks.add((j,y))
                for j in range(x, next_point[0]):
                    rocks.add((j, y))
                for j in range(y, next_point[1]):
                    rocks.add((x, j))
                for j in range(next_point[1], y):
                    rocks.add((x, j))
enum_rocks()
ymax = max(r[1] for r in rocks)
floor = ymax+2
def print_outcome(rocks, sand, starting):
    xmin = min(r[0] for r in rocks)
    xmax = max(r[0] for r in rocks)
    ymin = min(min(r[1] for r in rocks), 0)
    ymax = max(r[1] for r in rocks)
    
    grid = [["." for _ in range(xmin, xmax+1)] for _ in range(ymin, ymax + 1)]

    # add rocks:
    for rock in rocks:
        x = rock[0] - xmin
        y = rock[1] - ymin
        grid[y][x] = '#'

    # add sand
    for s in sand:
        x = s[0] - xmin
        y = s[1] - ymin
        grid[y][x] = 'o'

    # add falling path
    for p in falling_path:
        x = p[0] - xmin
        y = p[1] - ymin
        grid[y][x] = '~'

    # add starting
    grid[starting[1]-ymin][starting[0]-xmin] = '+'

    for y in grid:
        print("".join(y)+ "\n")

def is_rock(p):
    return p in rocks
def is_sand(p):
    return p in sand
def is_floor(p): 
    return p[1] == floor
def is_blocked(p):
    return is_rock(p) or is_sand(p) or is_floor(p)

def fall(p):
    x,y = p
    new_p = (x,y+1)
    if not is_blocked(new_p):
        return new_p;
    new_p = (x-1, y+1)
    if not is_blocked(new_p):
        return new_p
    new_p = (x+1, y+1)
    if not is_blocked(new_p):
        return new_p
    return p

def fall_grain(starting):
    new_p = starting
    while new_p[1] < ymax:
        old_p = new_p
        new_p = fall(new_p)
        if old_p == new_p:
            # blocked, store p and restart
            sand.add(new_p)
            #print_outcome(rocks, sand, starting)
            new_p = starting

    new_p = starting
    while new_p[1] < ymax:
        old_p = new_p
        new_p = fall(new_p)
        falling_path.add(new_p)
        

def fall_grain_floor(starting):
    new_p = starting
    while True:
        old_p = new_p
        new_p = fall(new_p)
        if old_p == new_p:
            # blocked, store p and restart
            sand.add(new_p)
            #print_outcome(rocks, sand, starting)
            new_p = starting
            if old_p == starting:
                break;
            
            
# TODO dynamic program this to fill up from the bottom. 
# find all the edges that fall in the area of sand
# add those spots to a set
# move upward to add subsequent edges until all edges that have been contained are managed
# find set.
def find_sand(point, floor):
    points = set()
    x, y = point
    spread = 0
    height = 0
    points.add(point)
    while height != floor:
        for i in range(x-spread, x+spread+1):
            points.add((i, y+height))
        height += 1
        spread += 1
    return points


def all_spaces():
    all_spaces = 0
    for path in rock_paths:
        for i, point in enumerate(path):
            x = point[0]
            y = point[1]
            if i != len(path)-1:  # If we aren't at the end connect the dots
                next_point = path[i+1]
                all_spaces += find_space_count(point,next_point, floor)
    return all_spaces


def find_space_count(point1,point2, floor):
    points = set()
    if (point1[0] == point2[0]):
        return 0
    x_distance = abs(point1[0]-point2[0])+1
    if (x_distance < 3):
        return 0;
    y = point1[0]
    height = 1
    spaces = 0
    while y+height != floor-1 and x_distance > 1:
        x_distance = x_distance - 2*height
        spaces += x_distance
        height+=1
        
    return spaces


all_possible_points = len(find_sand((500, 0), floor))
print(all_possible_points - all_spaces() - len(rocks))
#all possible - rocks - each x path inverted
# assumes there's no cavities thats a failure
fall_grain((500, 0))
#print_outcome(rocks,sand,(500,0))
print("Part 1: ",len(sand))
sand = set()
falling_path = set()
fall_grain_floor((500,0))
print()
print("Part 2: ",len(sand))

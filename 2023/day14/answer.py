import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer
from navigation import north, south, east, west
filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    dish = []
    rocks = {}
    cubes = {}
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    max_y = len(lines)
    for y, line in enumerate(lines):
        max_x = len(line)
        dish.append([])
        for x, space in enumerate(line):
            dish[y].append(space)
            if space =='O':
                rocks[(x,y)]  = True
            if space == '#':
                cubes[(x,y)] = True
    return dish, rocks, cubes, (max_x, max_y)

def in_bounds(point, maxes):
    x,y = point
    return x >= 0 and x< maxes[0] and y >=0 and y<maxes[1]

def get_point(dish, point):
    return dish[point[1]][point[0]]

def move_rock(dish, point, maxes, direction):
    def p(p):
        return get_point(dish, p)        
    curr = point
    next = direction(curr)
    while in_bounds(next, maxes) and not (p(next) == 'O' or p(next) == '#'):
        curr = next
        next = direction(curr)
    dish[point[1]][point[0]] = '.'
    dish[curr[1]][curr[0]] = 'O'

def tilt_column(row, direction):
    if 'O' not in row:
        return list(row);
    if direction == south or direction == east:
        row = list(row)
        row.reverse()
    new_column = ['.']*len(row)
    start_index = 0
    for i, space in enumerate(row):
        if space == 'O':
            new_column[start_index] = space
            start_index +=1
        elif space == '#':
            new_column[i] = '#'
            start_index = i+1
    if direction == south or direction == east:
        new_column.reverse()
    return new_column

def getColumn(grid, column):
    return [row[column] for row in grid]
def getRow(grid, row):
    return grid[row]
def insertColumn(grid, column, index):
    for i, row in enumerate(grid):
        row[index] = column[i]
def insertRow(grid, row, index):
    grid[index] = row

def tilt_fast(dish, maxes, direction):
    if direction == north:
        for i in range(maxes[1]):
            c = getColumn(dish, i)
            c = tilt_column(tuple(c), direction)
            insertColumn(dish, c, i)
    if direction == south:
        for i in range(maxes[1]):
            c = getColumn(dish, i)
            c = tilt_column(tuple(c), direction)
            insertColumn(dish, c, i)
    if direction == west:
        for i in range(maxes[1]):
            c = getRow(dish, i)
            c = tilt_column(tuple(c), direction)
            insertRow(dish, c, i)    
    if direction == east:
        for i in range(maxes[1]):
            c = getRow(dish, i)
            c = tilt_column(tuple(c), direction)
            insertRow(dish, c, i)    

def tilt(dish, maxes, direction):
    if direction == south or direction == east:
        for y in range(maxes[1]-1, -1, -1):
            for x in range(maxes[0]-1, -1, -1):
                space = dish[y][x]
                if space == 'O':
                    move_rock(dish, (x,y), maxes, direction)
    
    else:
        for y in range(maxes[1]):
            for x in range(maxes[0]):
                space = dish[y][x]
                if space == 'O':
                    move_rock(dish, (x,y), maxes, direction)

def tilt_faster(rocks, cubes,  maxes, direction):
    if direction == south or direction == east:
        for y in range(maxes[1]-1, -1, -1):
            for x in range(maxes[0]-1, -1, -1):
                if (x,y) in rocks:
                    move_rock_faster(rocks, (x,y), cubes, maxes, direction)
    
    else:
        for y in range(maxes[1]):
            for x in range(maxes[0]):
                if (x,y) in rocks:
                    move_rock_faster(rocks, (x,y), cubes, maxes, direction)

def move_rock_faster(rocks, point, cubes, maxes, direction):
    curr = point
    next = direction(curr)
    while in_bounds(next, maxes) and not ( next in rocks or next in cubes):
        curr = next
        next = direction(curr)
    del rocks[point]
    rocks[curr] = True



def cycle(dish, rocks, cubes, maxes):
    cyc = [north, west, south, east]
    for c in cyc:
        #tilt_faster(rocks,cubes, maxes, c)
        tilt_fast(dish, maxes, c)
        #tilt(dish, maxes, c)
def part1(dish, rocks, cubes, maxes):
    tilt_faster(rocks, cubes, maxes, north)  
    c = 0
    
    for r in rocks.keys():
        c += maxes[1]-r[1]
    
    print("Part 1: ",c)
    

@timer
def part2(dish, rocks, cubes, maxes):
    for i in range(1000):
        cycle(dish,rocks, cubes, maxes)
        c= 0
        for j, row in enumerate(dish):
            for x in row:
                if x == 'O':
                    c += maxes[1]-j
        print(i, c)
    print("Part 2: ",c)

part1(*prep())
print()
part2(*prep())
import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day9/inputs/actual.txt"

heightmap = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    heightmap.append([int(x) for x in list(line_data)])

def find_basin(x,y, matrix, basin):
    pt = matrix[y][x]
    xmax = len(matrix[0])
    ymax = len(matrix)
    if pt == 9:
        return basin
    else:
        if not ((x,y) in basin):
            basin.add((x,y))
            if (x+1) < xmax:
                find_basin(x+1,y, matrix, basin)
            if (y+1) < ymax:
                find_basin(x, y+1, matrix, basin)
            if (x-1) >= 0:
                find_basin(x-1,y, matrix, basin)
            if (y-1) >= 0:
                find_basin(x, y-1, matrix, basin)
        return basin
    pass

def get_adjecents(x,y, matrix):
    adjacents = []
    xmax = len(matrix[0])
    ymax = len(matrix)
    if (x+1) < xmax:
        adjacents.append(matrix[y][x+1])
    if (y+1) < ymax:
        adjacents.append(matrix[y+1][x])
    if (x-1) >= 0:
        adjacents.append(matrix[y][x-1])
    if (y-1) >= 0:
        adjacents.append(matrix[y-1][x])
    return adjacents

def is_low(x,y, matrix):
    pt = matrix[y][x]
    adjacents = get_adjecents(x, y, matrix);
    low = functools.reduce(lambda r, v: r and pt < v, adjacents, True)
    if low:
        print(pt, get_adjecents(x, y, matrix))
    return low

lows =[]
basins = []
for x in range(len(heightmap[0])):
    for y in range(len(heightmap)):
        if is_low(x,y,heightmap):
            lows.append(heightmap[y][x])
            basin = set()
            basins.append(find_basin(x,y, heightmap, basin))

print("Part 1: ",sum(lows) + len(lows))
print()
print("Part 2: ", functools.reduce(lambda r, v: r*v,
      sorted([len(basin) for basin in basins], reverse=True)[:3], 1))

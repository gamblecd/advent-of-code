import fileinput, bisect
import functools
from collections import defaultdict
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day13/inputs/actual.txt"
grid = defaultdict(lambda: '.')
instructions = []
empty = False
xmax = 0
ymax = 0
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if line_data == "":
        empty = True
        continue
    if not empty:
        x,y =  (int(x)for x in line_data.split(","))
        xmax = max(x, xmax)
        ymax = max(y, ymax)
        grid[(x,y)] = "#"
    else:
        instructions.append(line_data.split(" ")[2])
        

def print_mapped_grid(grid, xmax,ymax):
    for y in range(ymax+1):
        line = ""
        for x in range(xmax+1):
            if (x,y) in grid.keys():
                line += grid[(x,y)]
            else:
                line += "."
        print(line)            
def fold(grid, command, xmax, ymax):
    direction, line = command.split("=")
    line = int(line)
    if (direction == 'y'):
        for (x,y) in list(grid.keys()):
            if (y >= line):
                ynew = line - (y-line)
                dot = grid[(x,y)]
                grid[(x,ynew)] = dot
                grid.pop((x,y))
        return (xmax, line-1)
    if (direction == 'x'):
        for (x,y) in list(grid.keys()):
            if (x >= line):
                xnew = line - (x-line)
                dot = grid[(x,y)]
                grid[(xnew,y)] = dot
                grid.pop((x,y))
        return (line-1, ymax)
for instr in instructions:
    xmax,ymax = fold(grid, instr, xmax, ymax)
print("Part 1: ",len(grid.keys()))
print()
print("Part 2: ",print_mapped_grid(grid, xmax, ymax)
)

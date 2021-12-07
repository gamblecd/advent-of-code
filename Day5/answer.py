import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day5/inputs/ex.txt"

xmax = 0
ymax = 0
vent_map = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    pts = line_data.split(" -> ")
    xy1,xy2 = pts[0], pts[1]
    xy1split = xy1.split(",")
    xy2split = xy2.split(",")
    x1, y1 = (int(xy1split[0]), int(xy1split[1]))
    x2, y2 = (int(xy2split[0]), int(xy2split[1]))
    vent_map.append((x1, y1), 
                    (x2, y2))
print(vent_map)

map = [[0 for i in range(xmax+1)] for i in range(ymax+1)]

print("Part 1: ",)
print()
print("Part 2: ",)

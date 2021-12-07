import fileinput, bisect
import functools
import os
import sys
from collections import Counter
import numpy as np

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day5/inputs/actual.txt"

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
    xmax = max(x1, x2, xmax)
    ymax = max(y1, y2, ymax)
    vent_map.append(((x1, y1), 
                    (x2, y2)))
#print(vent_map, xmax, ymax)

def is_col(t):
    return t[0][0] == t[1][0]

def is_row(t):
    return t[0][1] == t[1][1]

def expand_line(t, part2=False):
    t1 = t[0]
    t2 = t[1]
        
    if is_row(t):
        if t1[0] > t2[0]:
            swap = t1
            t1 = t2
            t2 = swap
    elif is_col(t):
        if t1[1] > t2[1]:
            swap = t1
            t1 = t2
            t2 = swap    
    else:
        if not part2:
            return []
        x1 = t1[0]
        x2 = t2[0]
        y1 = t1[1]
        y2 = t2[1]
        pos = x2 - x1;
        xstep = pos // abs(pos);
        x2 += pos // abs(pos)
        pos = y2 - y1;
        ystep = pos // abs(pos);
        y2 += pos // abs(pos)

        line = list(zip([x for x in range(x1, x2,xstep)], [y for y in range(y1, y2,ystep) ]))
        return line
    return [(x,y) for x in range(t1[0], t2[0]+1) for y in range(t1[1], t2[1]+1)]

def analyze_map(m):
    return len(list(map( lambda x: x[0], filter(lambda x:x[1]>=2, list(m.most_common())))))

def build_map(part2=False):
    m = []
    for vent in vent_map:
        m.extend(expand_line(vent, part2))
        #print(max(m, key=list.count))
    return Counter(m)

print("Part 1: ", analyze_map(build_map()))
print()
print("Part 2: ",analyze_map(build_map(True)))

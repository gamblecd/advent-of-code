import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import print_grid, get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    galaxies = []
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    max_y = len(lines)
    for y, line in enumerate(lines):
        max_x = len(line)
        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((x,y))
    return galaxies, (max_x,max_y)

def expand(galaxies, maxes, rate=2):
    # rows
    rows = []
    columns = []
    for y in range(maxes[1]):
        do_expand = True
        for g in galaxies:
            if g[1] == y:
                do_expand = False
        if do_expand:
            rows.append(y)
    for x in range(maxes[0]):
        do_expand = True
        for g in galaxies:
            if g[0] == x:
                do_expand = False
        if do_expand:
            columns.append(x)
            
    new_galaxies = []
    for g in galaxies:
        x,y = g
        new_x = x + (rate-1) * (bisect.bisect(columns, x))
        new_y = y + (rate-1) * (bisect.bisect(rows, y))
        new_galaxies.append((new_x, new_y))
#    print(rows, columns)
    return new_galaxies, (maxes[0] + (rate-1) * len(columns), maxes[1] + (rate-1) * len(rows))

def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1] - p2[1])
 
def galactic_pairs(galaxies):
    pairs = set()
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i+1:]:
            if g1 != g2:
                pairs.add((g1,g2))
    return pairs
def part1(galaxies, maxes):
    galaxies, maxes = expand(galaxies, maxes)
    s = 0
    for p1, p2 in galactic_pairs(galaxies):
        s += distance(p1,p2)
    print("Part 1: ",s)

def part2(galaxies, maxes):
    galaxies, maxes = expand(galaxies, maxes, 1000000)
    #print(maxes)
    #print_grid((0,0), maxes, ".", [('#', galaxies)])
    s = 0
    for p1, p2 in galactic_pairs(galaxies):
        s += distance(p1,p2)
    print("Part 1: ",s)

part1(*prep())
print()
part2(*prep())
import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..','..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = os.path.join(script_dir, "inputs", "actual.txt");

curr = 0
elves= [0]

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if not line_data:
        curr += 1
        elves.append(0)
    else:
        elves[curr] = elves[curr] + int(line_data)


print("Part 1: ",max(elves))
print()
s = 0
for _ in range(3):
    s += elves.pop(elves.index(max(elves)))

print("Part 2: ",s)

import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join(script_dir, '..', '..', 'utils')
sys.path.append(mymodule_dir)

from util import timer_func as timer
args = sys.argv[1:]
run_actual = len(args) >= 1 and args[0] == "PROD"
if (run_actual):
    filename = os.path.join(script_dir, "inputs", "actual.txt")
else:
    filename = os.path.join(script_dir, "inputs", "ex.txt")

def contains(ind, ind2):
    return ind[0]<= ind2[0] and ind[1]>= ind2[1]

def overlaps(ind, ind2):
    return ind[0] <= ind2[0] <= ind[1] or ind[0] <= ind2[1] <= ind[1]

total = 0
part2 = 0
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    indexes = line_data.split(",");
    indexes1, indexes2 = indexes[0].split("-")
    indexes1 = (int(indexes1), int(indexes2))
    indexes3, indexes4 = indexes[1].split("-")
    indexes2 = (int(indexes3), int(indexes4))
    
    if contains(indexes1, indexes2) or contains(indexes2, indexes1):
       total += 1
    if overlaps(indexes1, indexes2) or overlaps(indexes2, indexes1):
       part2 += 1
    
print("Part 1: ", total)
print()
print("Part 2: ", part2)

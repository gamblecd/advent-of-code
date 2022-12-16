import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
args = sys.argv[1:]
run_actual = len(args) >= 1 and args[0] == "PROD"
if (run_actual):
    filename = os.path.join(script_dir, "inputs", "actual.txt")
else:
    filename = os.path.join(script_dir, "inputs", "ex.txt")

values = '0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_value(f):
    return values.index(f)

total = 0

rucksacks = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    length = len(line_data)
    compartment1 = line_data[:length // 2]
    compartment2 = line_data[length // 2 :]
    rucksacks.append(line_data)
    s = set();
    for x in compartment1:
        if x in compartment2:
            s.add(x)
    
    for x in s:        
        total += get_value(x)
        
part2 = 0
for x in rucksacks[::3]:
    i = rucksacks.index(x)
    print(i, x)
    s = set()
    for y in x:
        if y in rucksacks[i+1] and y in rucksacks[i+2]:
            s.add(y)
    for y in s:
        part2 += get_value(y)             
print("Part 1: ", total)
print()
print("Part 2: ", part2)

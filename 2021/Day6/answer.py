import fileinput, bisect
import functools
import os
import sys
from collections import Counter, defaultdict
script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day6/inputs/actual.txt"

initial_state = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    initial_state = [int(x) for x in line_data.split(",")]


part2_state = initial_state.copy();

@timer
def run_fast(time):
    global initial_state
    part2_state = initial_state.copy();
    part2_state = dict(Counter(part2_state))
    for i in range(time):
        new_state = defaultdict(int)
        for key, value in part2_state.items():
            if (key == 0):
                new_state[6] += value
                new_state[8] += value;
            else:
                new_state[key-1] += value
        part2_state = new_state
    return sum(part2_state.values());

@timer
def run_brute_force(time):
    global initial_state
    part1_state = initial_state.copy();
    zeros = 0
    for i in range(time):
        part1_state = sorted(list(map(lambda x: 6 if x==0 else x-1, part1_state)));
        part1_state += [8] * zeros
        zeros = part1_state.count(0)
    return len(part1_state)
    
print("Part 1: ",run_fast(80))
print()
print("Part 2: ",run_fast(256))

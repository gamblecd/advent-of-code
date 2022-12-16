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

start_of_packet_marker_size = 4
start_of_message_marker_size = 14
@timer
def find_marker(line, marker_size):
    for i in range(len(line) - marker_size):
        sl = line[i:i+marker_size]
        s = set()
        for j in sl:
            s.add(j)
        if len(s) == marker_size:
            return i+marker_size

part1 = []
part2 = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    part1.append(find_marker(line, start_of_packet_marker_size))
    part2.append(find_marker(line, start_of_message_marker_size))
    
    
print("Part 1: ", part1[0])
print()
print("Part 2: ", part2[0])

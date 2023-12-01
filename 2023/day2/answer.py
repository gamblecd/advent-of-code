import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = []
    for line in fileinput.input(files=(filename)):
        line_data = line.strip()
        lines.append(line_data)
    return lines

def part1(lines):
    for line in lines:
        pass
    print("Part 1: ",)

def part2(lines):
    for line in lines:
        pass
    
    print("Part 2: ",)

part1(prep());
print()
part2(prep());
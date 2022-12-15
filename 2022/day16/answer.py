import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    
print("Part 1: ",)
print()
print("Part 2: ",)
import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "DayX/inputs/ex.txt"

for line in fileinput.input(files=(filename)):
    line_data = line.strip()

    
print("Part 1: ",)
print()
print("Part 2: ",)

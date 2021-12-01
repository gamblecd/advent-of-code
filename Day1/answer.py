import fileinput
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day1/inputs/actual.txt"

depths = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    depth = int(line_data)
    depths.append(depth)

# O(N) Solution assuming get_depth remains O(1) lookup
@timer
def calculate_depths(depths, get_depth=lambda x,y:y[x]):
    previous_depth = None
    increasing_count = 0
    for index in range(len(depths)):
        depth = get_depth(index, depths)
        if not (previous_depth == None or depth == None):
            if depth > previous_depth:
                increasing_count = increasing_count + 1
        #         print('{depth} (increased)'.format(depth=depth))
        #     elif val == previous_depth:
        #         print('{depth} (no change)'.format(depth=depth))
        # else:
        #     print('{depth} (N/A - no previous measurement)'.format(depth=depth))
        previous_depth = depth
    return increasing_count

def add_next_2(index,arr):
    if len(arr)-2 <= index:
        return None
    return arr[index] + arr[index +1] + arr[index+2]

# Find how quickly the depth is increasing 
print("Part 1: ", calculate_depths(depths))
print()
#Using 3 value average to determine depth
print("Part 2: ", calculate_depths(depths, add_next_2))
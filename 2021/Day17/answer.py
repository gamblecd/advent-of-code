import fileinput, bisect
from collections import defaultdict
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day17/inputs/actual.txt"

targets = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    line = line.replace(",", "")
    x,y = line.split()[2:4]
    x1, x2 = x.split("=")[1].split("..")
    y1, y2 = y.split("=")[1].split("..")
    targets.append(((int(x1), int(y1)), (int(x2), int(y2))))
    
def find_y_velocities(x_velocities, target1, target2):
    max_y = target2[1]
    min_y = target1[1]
    y_max = 0
    possible_velocities = {}
    discrete_x_velocities =x_velocities[0]
    likely_velocities = sorted(discrete_x_velocities.items(), key=lambda x: len(x[1]), reverse=True)
    non_discrete_x_velocities = x_velocities[1]
    for x_velocity, steps in likely_velocities:
        # TODO some set of ranges for y
        for y in range(-max(abs(max_y), abs(min_y)), max(abs(max_y), abs(min_y))):
            velocity = y
            for x_step in steps:
                y_loc = sum([velocity-xs for xs in range(0,x_step)])
                y_height = sum(
                    filter(lambda x: x > 0, [velocity-xs for xs in range(0, x_step)]))
                if y_loc >= min_y and y_loc <= max_y:
                    y_max = max(y_max, y_height)
                    possible_velocities[(x_velocity, y)] = y_height
    
    for x_velocity, steps in non_discrete_x_velocities.items():
        # TODO some set of ranges for y
        for y in range(-max(abs(max_y), abs(min_y)), max(abs(max_y), abs(min_y))):
            velocity = y
            initial_step = steps[0]
            y_loc = max_y
            while y_loc >= min_y:
                y_loc = sum([velocity-xs for xs in range(0, initial_step)])
                y_height = sum(
                    filter(lambda x: x > 0, [velocity-xs for xs in range(0, initial_step)]))
                if y_loc >= min_y and y_loc <= max_y:
                    y_max = max(y_max, y_height)
                    possible_velocities[(x_velocity, y)] = y_height
                initial_step += 1

    return y_max, len(possible_velocities.keys())

def find_x_velocities(target1, target2):
    max_x = target2[0]
    min_x = target1[0]
    possible_discrete_velocities = defaultdict(lambda: [])
    possible_non_discrete_velocities = defaultdict(lambda: [])
    for x in range(max_x+1):
        x_loc = x
        velocity = x
        old_velocity = 0
        step = 1
        # TODO handle negative case?
        while x_loc <= max_x and old_velocity != velocity:
            if x_loc >= min_x and x_loc <= max_x:
                if (velocity == 0):
                    possible_non_discrete_velocities[x].append(step-1)
                else:
                    possible_discrete_velocities[x].append(step)
            old_velocity = velocity
            if (velocity > 0):
                velocity -= 1
            elif (velocity < 0):
                velocity += 1
            x_loc += velocity
            step += 1
    
    return possible_discrete_velocities, possible_non_discrete_velocities
print(targets)
x_velocities = find_x_velocities(targets[0][0], targets[0][1])
print(find_y_velocities(x_velocities, targets[0][0], targets[0][1]))



print("Part 1: ",)
print()
print("Part 2: ",)

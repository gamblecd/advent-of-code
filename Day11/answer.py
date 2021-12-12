import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer, print_grid
filename = "Day11/inputs/actual.txt"
octopi = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    octopi.append([int(x) for x in list(line_data)])

flashers = []

def reset(flashers, matrix):
    for x,y in flashers:
        matrix[y][x] = 0

def flash(x,y, matrix, flashers):
    xmax = len(matrix[0])
    ymax = len(matrix)
    is_left = not (x-1) >=0
    is_top = not (y-1) >=0
    is_right = not x+1 < xmax
    is_bottom = not y+1 < ymax
    
    x_options = [-1,0,1]
    if is_left:
        x_options.remove(-1)
    if is_right:
        x_options.remove(+1)
    y_options = [-1,0,1]
    if is_top:
        y_options.remove(-1)
    if is_bottom:
        y_options.remove(+1)
    
    for n in x_options:
        for m in y_options:
            if not (n == 0 and m == 0):
                nx,ny = x+n, y+m
                if increase(nx, ny, matrix):
                    flashers.append((nx,ny))
    return flashers

def increase(x,y, matrix):
    v = matrix[y][x] + 1
    matrix[y][x] = v
    return v == 10
print_grid(octopi)

s = 0
synchronized = False;
steps = 0
while not synchronized:
    flashers = []
    #Step 1: increase all numbers
    for y in range(len(octopi)):
        for x in range(len(octopi[y])):
            if increase(x,y,octopi):
                flashers.append((x,y))
                
                

    # Step2: flash all valid ones
    all_flashers = set(flashers)
    while not len(flashers) == 0:
        flashers_swap = []
        for popx,popy in flashers:
            flash(popx,popy, octopi, flashers_swap)
            flashers = set(flashers_swap).difference(all_flashers)
        #print_grid(octopi)
        all_flashers = all_flashers.union(flashers_swap)
    synchronized = len(all_flashers) == len(octopi) * len(octopi[0])
    #Step 3 Reset
    reset(all_flashers, octopi)
    if (steps < 100):
        s += len(all_flashers)
    #print_grid(octopi)
    steps +=1
print("Part 1: ", s)
print()
print("Part 2: ",steps)

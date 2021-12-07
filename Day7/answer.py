import fileinput, bisect
import functools
import os
import sys
from statistics import multimode, median, mean

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day7/inputs/actual.txt"

horizontal_positions = None
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    horizontal_positions = sorted([int(x) for x in line_data.split(",")])

mode = multimode(horizontal_positions)
def calc_fuel(distance):
    f=0
    for d in range(distance+1):
        f += 1*d
    return f

fuelcosts = {}
def calc_fuel_memo(distance):
    global fuelcosts
    f = 0
    if distance in fuelcosts:
        return fuelcosts[distance]
    for d in range(distance+1):
        f += 1*d
    fuelcosts[distance] = f;
    return f
@timer
def part_one():
    global horizontal_positions
    avg = median(horizontal_positions)
    return functools.reduce(lambda r,v: r + abs(v-(avg//1)), horizontal_positions, 0)

@timer
def part_two():
    global horizontal_positions
    me = mean(horizontal_positions)
    return functools.reduce(lambda r,v: r + calc_fuel(int(abs(v-(round(me))))), horizontal_positions, 0)
@timer
def part_two_memo():
    global horizontal_positions
    me = mean(horizontal_positions)
    print(round(me//1))
    return functools.reduce(lambda r,v: r + calc_fuel_memo(int(abs(v-(round(me//1))))), horizontal_positions, 0)

print("Part 1: ",part_one())
print()
print("Part 2: ",part_two(), part_two_memo())

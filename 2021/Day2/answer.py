import fileinput, bisect, operator
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day2/inputs/actual.txt"

commands = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    command, amt_str = line_data.split()
    amt = int(amt_str)
    commands.append((command, amt))

oper = {"forward": operator.add, "down":operator.add, "up": operator.sub}

@timer
def part_1():
    h1,d1 = 0,0
    for t in commands:
        command = t[0]
        amt = t[1]
        if command == "forward":
            h1 = oper[command](h1, amt)
        else:
            d1 = oper[command](d1, amt)
    return h1 * d1

@timer
def part_2():
    global oper
    h2,d2,aim2 = 0,0,0
    for t in commands:
        command = t[0]
        amt = t[1]
        if command == "forward":
            h2 = oper[command](h2, amt)
            d2 = d2 + (amt * aim2)
        else:
            aim2 = oper[command](aim2, amt)
    return h2 * d2
    
print("Part 1: ", part_1())
print()
print("Part 2: ", part_2())

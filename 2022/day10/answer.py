import fileinput, bisect
import functools
import queue
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

registry = 1
crt = ["." * 40]
crt_row = []
cycle_values = [20,60,100,140, 180, 220]
execution_queue = queue.Queue()
increment = queue.Queue()
row=1

def execute_cycle():
   
    increment_cycle()
    cmd, val = execution_queue.get()
    if cmd == "noop":
        pass
    else:
        increment_cycle()
        increment.put(val)

def increment_cycle():
    global cycle, s, crt_row, row
    index = len(crt_row)
    if registry-1 <= index <= registry + 1:
        crt_row.append("#")
    else:
        crt_row.append(".")


    cycle += 1 
    if cycle % 40 == 0:
        print("".join(crt_row))
        row += len(crt_row)
        crt_row = []

    if cycle in cycle_values:
        #print(cycle, registry, cycle * registry)
        s += cycle * registry

def execute_after_cycle():
    global registry
    if not increment.empty():
        registry += increment.get()
    pass

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    line_split = line_data.split()
    cmd, val = None, None
    if len(line_split) == 1:
        # noop
        cmd = line_split[0]
        pass
    else:
        # addx
        cmd, val = line_split
        val = int(val)
    execution_queue.put((cmd, val))

cycle = 0
s = 0
while not execution_queue.empty():
    execute_cycle()
    execute_after_cycle()
    
print("Part 1: ",s)
print()
print("Part 2: ",)

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

dirs = []

root = {"name":"/", "parent": None, "dirs":{}, "files": {}}

current = root;

total_space = 70000000;
target_free_space = 30000000;
def parseCommand(line):
    cmdParts = line.split()
    cmd = cmdParts[1]
    location = cmdParts[2]
    return (cmd, location)

def gatherSize(dir):
    size = 0
    for f in dir['files'].values():
        size += f['size']
       
    for d in dir['dirs'].values():
        if 'size' not in d.keys():
            gatherSize(d)
        size += d['size']
    dir['size'] = size    
    dirs.append(dir)
    return size

def executeCD(loc):
    global current;
    if loc == "..":
        # before we go up lets see if we can get the size of current.
        # Optimization
        #gatherSize(current)
        
        current = current['parent']
    elif loc == "/":
        current = root;
    else:
        current = current['dirs'][loc]
        

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if line_data[0] == '$':
        cmd = line_data.split();
        if len(cmd) == 3:
            loc = cmd[2]
            executeCD(loc)
    else:
        output, name = line_data.split()
        if output == "dir":
            current['dirs'][name] = {'name': name, "parent": current, "dirs": {}, "files": {}}
        else:
            current['files'][name] = {"name": name, "size": int(output)}

@timer
def gatherRoot():
    global root;
    gatherSize(root)

gatherRoot();

dirs.sort(key=lambda x: x['size'], reverse=True)
dirs.pop(0)

t = 0

actual_space = total_space - root['size']
goal = target_free_space - actual_space
target = None
for i, d in enumerate(dirs):
    size = d['size']
    if size <= 100000:
        t += size
    if not target and size <= goal:
        target = dirs[i-1]
print("Part 1: ", t)
print()
print("Part 2: ",target['size'])

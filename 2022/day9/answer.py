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
    filename = os.path.join(script_dir, "inputs", "ex2.txt")

starting = (0,0)
chain1 = [starting, starting]
chain2 = [starting for _ in range(10)]
dirs = {'R': (1,0), 'U': (0,1), 'D':(0,-1), 'L': (-1,0)}

unique_locations = set({starting})

def is_touching(head, tail):
    hx,hy = head
    tx,ty = tail
    return hx-1 <= tx <= hx+1 and hy-1 <= ty <= hy+1

def move_next(head, tail):
    hx, hy = head
    tx, ty = tail
    x_diff = (hx-tx)
    y_diff = (hy - ty)
    next_dir = (x_diff if x_diff == 0 else (hx-tx) // abs(hx-tx),
        y_diff if y_diff == 0 else (hy - ty) // abs(hy-ty))
    return tail[0] + next_dir[0], tail[1] + next_dir[1]

def move_chain(chain, dir):
    chain[0] = move_head(chain[0], dir)
    head = chain[0]
    for i, x in enumerate(chain[1:]):
        if not is_touching(head, x):
            chain[i+1] = move_next(head, x)
        else:
            # can we shortcut this? I think we can
            return chain
        head = chain[i+1]
    return chain

def move_head(head, dir):
    return head[0] + dir[0], head[1] + dir[1]

def make_move(chain, dir, count):
    global unique_locations;
    global starting;
    for _ in range(count):
        chain = move_chain(chain, dirs[dir])
        unique_locations.add(chain[-1])
    return chain

@timer
def execute(chain):
    for line in fileinput.input(files=(filename)):
        line_data = line.strip()
        dir, count = line_data.split()
        count = int(count)
        chain = make_move(chain, dir, count)

execute(chain1)
print("Part 1: ", len(unique_locations))
unique_locations = set({starting})
execute(chain2)
print("Part 2: ", len(unique_locations))
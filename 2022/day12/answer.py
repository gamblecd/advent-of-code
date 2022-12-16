import fileinput, bisect
import functools
import os
import sys
import queue

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

grid = []
start = None
end = None
shortest_path = {}

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    grid.append([ ord(x) for x in line_data])
    if 'S' in line_data:
        start = (line_data.index('S'), len(grid) - 1)
        grid[start[1]][start[0]] = ord('a')
    if 'E' in line_data:
        end = (line_data.index('E'), len(grid) - 1)
        grid[end[1]][end[0]] = ord('z')

def elev(point):
    return grid[point[1]][point[0]]

def can_traverse(x, y):
    return elev(x) + 1 >= elev(y)

def get_adjecents(point, matrix, fil= lambda x:True):
    x,y = point
    adjacents = []
    xmax = len(matrix[0])
    ymax = len(matrix)
    if (x+1) < xmax:
        adjacents.append((x+1, y))
    if (y+1) < ymax:
        adjacents.append((x, y+1))
    if (x-1) >= 0:
        adjacents.append((x-1, y))
    if (y-1) >= 0:
        adjacents.append((x, y-1))
    return list(filter(fil, adjacents))

paths = queue.PriorityQueue()
visited = set()

def find_path_reverse(grid, condition):
    priority, path = paths.get()  # get the next shortest path
    point = path[0]
    if point in visited:
        return None
    if condition(point):
        return path
    visited.add(point)
    shortest_path[point] = priority
    for a in get_adjecents(point, grid, fil = lambda a: can_traverse(a, point)):
        if not a in path:
            if a in shortest_path.keys() and priority+1 > shortest_path[a]:
                continue
            new_path = [a]+path
            paths.put((len(new_path), new_path))
    return None

@timer
def reverse_cond(condition=lambda x: x == start):
    paths.put((1, [end]))
    rets = []
    path = None
    while not paths.empty():
        path = find_path_reverse(grid, condition)
        if path:
            rets.append(path)
    return rets

shortest_path = {}
visited = set()
paths = queue.PriorityQueue()
path = reverse_cond()[0]
print("Part 1: ", len(path)-1)

shortest_path = {}
visited = set()
paths = queue.PriorityQueue()
path = reverse_cond(condition=lambda x: chr(elev(x)) == 'a')[0]
print()
print("Part 2: ", len(path)-1)

import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day15/inputs/actual.txt"

sorted


grid = {}
noded_grid = {}
xmax=0
ymax=0
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    x = 0
    for n in line_data:
        grid[(x,ymax)] = int(n)
        noded_grid[(x,ymax)] = (int(n), None, True, [])
        x +=1
    xmax = max(xmax, x)
    ymax += 1

for y in range(ymax):
    for j in range(5):
        new_y = y + j*ymax
        for x in range(xmax):
            for i in range(5):
                new_x = x + i*xmax
                old_grid = noded_grid[(x,y)]
                new_value = (old_grid[0] + i + j)
                noded_grid[(new_x, new_y)] = (new_value % 9 if new_value > 9 else new_value , None, True, [])
xmax = 5*xmax
ymax = 5*ymax

def print_grid(noded_grid):
    for i in range(ymax):
        s = ""
        for j in range(xmax):
            s += str(noded_grid[(j,i)][0])
        print(s)

#print_grid(noded_grid)
def get_risk(chain):
    return sum(map(lambda x: int(grid[x]), chain))

def find_path_minimum(paths, grid):
    # Lowest path
    chain, risk = paths[0]
    location = chain[-1]
    if location == (xmax-1, ymax-1):
        return risk, True
    else:
        paths = paths[1:]
        chain
        x, y = location
        if x < xmax-1:
            newx = x + 1
            newLocation = (newx, y)
            newChain = chain + [newLocation]
            bisect.insort_left(
                paths, (newChain, risk + grid[newLocation]), key=lambda x: x[1])
        if y < ymax-1:
            newy = y + 1
            newLocation = (x, newy)
            newChain = chain + [newLocation]
            bisect.insort_left(
                paths, (newChain, risk + grid[newLocation]), key=lambda x: x[1])
        
        # if x_risk == None or (not y_risk == None and x_risk >= y_risk):
        #     newLocation = newLY
        # else:
        #     newLocation = newLX
        # newChain = [*chain, newLocation]
        # bisect.insort_left(paths, (newChain, risk + grid[newLocation]), key=lambda x:x[1])

        return paths, False


def find_path_node_minimum(nodes, grid):
    # Lowest path
    location = nodes[0]
    risk, total_risk, open, children = grid[location]
    if not open:
        pass

    if location == (xmax-1, ymax-1):
        grid[location] = (risk, total_risk, False, children)
        return nodes, True
    else:
        x, y = location
        if x < xmax-1:
            newx = x + 1
            newLocation = (newx, y)
            children.append(newLocation)
        if y < ymax-1:
            newy = y + 1
            newLocation = (x, newy)
            children.append(newLocation)

        if x > 0:
            newx = x-1
            newLocation = (newx, y)
            children.append(newLocation)
        if y > 0:
            newy = y - 1
            newLocation = (x, newy)
            children.append(newLocation)


        for child in children:
            child_set = grid[child]
            
            child_risk = child_set[0]
            child_total_risk = min(total_risk + child_risk, child_set[1]) if not child_set[1] is None else total_risk + child_risk
            child_set = (child_risk, child_total_risk,
                         child_set[2], child_set[3])
            grid[child] = child_set

            if not child in nodes and child_set[2]:
                bisect.insort_right(
                    nodes, child, key=lambda x: grid[x][1])
        nodes = nodes[1:]
        grid[location] = (risk, total_risk, False, children)
        return nodes, False


@timer
def find_min(grid):
    paths = [([(0, 0)], 0)]
    found = False
    while not found:
        paths, found = find_path_minimum(paths, grid)
    return paths


@timer
def find_min_node(grid):
    nodes = [(0, 0)]
    initial_node = grid[nodes[0]]
    grid[nodes[0]] = (initial_node[0],0,initial_node[2], initial_node[3])
    found = False
    while not found:
        nodes, found = find_path_node_minimum(nodes, grid)

    return grid[nodes[0]][1]

def find_path(chain, grid):
    location = chain[-1]
    if location == (xmax-1, ymax-1):
        return chain
    else:
        x,y = location
        newx,newy = x,y
        paths = []
        if x < xmax-1:
            newx = x + 1
            newLocation = (newx, y)
            if not newLocation in chain:
                newChain = [(newx, y)]
                paths.append(find_path(newChain, grid))
        # if x < 0:
        #     newx = x - 1
        #     newLocation = (newx, y)
        #     if not newLocation in chain:
        #         newChain = [(newx, y)]
        #         paths.append(find_path(newChain, grid))
        if y < ymax-1:
            newy = y + 1
            newLocation = (x, newy)
            if not newLocation in chain:
                newChain = [(x, newy)]
                paths.append(find_path(newChain, grid))
        # if y < 0:
        #     newy = y - 1
        #     newLocation = (x, newy)
        #     if not newLocation in chain:
        #         newChain = [(x, newy)]
        #         paths.append(find_path(newChain, grid))
        paths = list(filter(lambda x: x, paths))
        if len(paths) == 0:
            return None
        paths = list(zip(paths, map(lambda x: get_risk(x), paths)))
        lowest_risk = paths[0]
        for n in paths:
            if n[1] < lowest_risk[1]:
                lowest_risk = n
        return chain + lowest_risk[0]

@timer
def find_path_wrapper(grid):
    return get_risk(find_path([(0, 0)], grid)[1:])

#print(find_path_wrapper(grid))
#print(find_min(grid))
print("Part 1: ", find_min_node(noded_grid))
print()
print("Part 2: ",)

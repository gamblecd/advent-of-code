import fileinput
import functools
import operator
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

tree_grid = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    tree_row = [int(t) for t in line_data]
    tree_grid.append(tree_row)

row_edges = (0, len(tree_grid[0])-1)
column_edges = (0, len(tree_grid)-1)

def get_tree(tree):
    global tree_grid;
    return tree_grid[tree[1]][tree[0]] # y,x

def is_edge(tree):
    x, y = tree
    if x in row_edges or y in column_edges:
        return True

def is_tallest(tree, direction):
    if (len(direction) == 0):
        return True
    for t in direction:
        if t >= get_tree(tree):
            return False
    return True

def is_visible(tree):
    x,y = tree
    if is_edge(tree):
        return (True, 0)
    else:
        directions = get_directions(tree)
        for dir in directions: 
            if is_tallest(tree, dir):
                scenic_score = scenic(tree, directions)
                return (True, scenic_score)
        return (False, 0)


def count_until_blocked(tree_height, direction):
    if (len(direction) == 0):
        return 0;
    count = 0
    for t in direction:
        count += 1
        if t >= tree_height:
            return count
    return count

def get_directions(tree):
    global tree_grid
    return [ 
            tree_grid[tree[1]][tree[0]+1:], # -x
            [z for z in reversed(tree_grid[tree[1]][0:tree[0]])], # +x
            [tree_grid[i][tree[0]] for i in range(tree[1]+1, column_edges[1]+1)], # -y
            [z for z in reversed([tree_grid[i][tree[0]] for i in range(tree[1])])] # +y
     ]

def scenic(tree, directions = None):
    if not directions:
        directions = get_directions(tree)
    scenic_scores = []
    for directionArr in directions:
        scenic_scores.append(count_until_blocked(get_tree(tree), directionArr))
    return functools.reduce(operator.mul, scenic_scores, 1)

@timer
def exec(tree_grid):
    count = 0
    mostScenic = 0;
    for i, row in enumerate(tree_grid):
        for j, height in enumerate(row):
            visible, scenic = is_visible((j, i))
            if visible:
                mostScenic = max(mostScenic, scenic)
                count += 1
    return count, mostScenic

part1, part2 = exec(tree_grid);
print("Part 1: ", part1)
print()
print("Part 2: ", part2)
import fileinput, bisect
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


def is_taller(tree1, tree2):
    global tree_grid
    return get_tree(tree1) > get_tree(tree2)

def is_edge(tree):
    x, y = tree
    if x in row_edges or y in column_edges:
        return True

def is_outside(potential_fake_tree):
    x, y = potential_fake_tree
    if (x < row_edges[0] or x > row_edges[1]) or (y < row_edges[0] or y > row_edges[1]):
        return True

def is_visible(tree):
    x,y = tree
    if is_edge(tree):
        return True
    else:
        tree_directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dir in tree_directions:
            new_tree = tree
            tallest = True
            # For Each direction continue until we hit an edge
            while tallest and not is_edge(new_tree):
                new_tree = (new_tree[0]+dir[0], new_tree[1] + dir[1])
                tallest = is_taller(tree, new_tree)
            # Find if tallest tree in row
            if tallest:
                return True
        return False;

def count_until_blocked(tree_height, direction):
    if (len(direction) == 0):
        return 0;
    count = 0
    for t in direction:
        count += 1
        if t >= tree_height:
            return count
    return count


def increment_tree(tree, dir):
    return (tree[0]+dir[0], tree[1] + dir[1])

def scenic(tree):
    global column_edges;
    global tree_grid
    first_tree = tree
    if is_visible(tree) and not is_edge(tree):
        scenic_scores = []
        tree_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x,y in tree_directions:
            directionArr = []
            if x == 1:
                directionArr  = tree_grid[tree[1]][tree[0]+1:]
            elif x == -1:
                directionArr = tree_grid[tree[1]][0:tree[0]]
                directionArr = [z for z in reversed(directionArr)]
            elif y == 1:
                for i in range(tree[1]+1, column_edges[1]+1):
                    directionArr.append(tree_grid[i][tree[0]])

            else: 
                for i in range(tree[1]):
                    directionArr.append(tree_grid[i][tree[0]])
                directionArr = [z for z in reversed(directionArr)]
            scenic_scores.append(count_until_blocked(get_tree(tree), directionArr))
        return functools.reduce(operator.mul, scenic_scores, 1)
    return 0

@timer
def part1(tree_grid):
    count = 0
    for i, row in enumerate(tree_grid):
        for j, height in enumerate(row):
            if is_visible((j, i)):
                count += 1
    return count

@timer
def part2(tree_grid):
    best_score = 0
    for i, row in enumerate(tree_grid):
        for j, height in enumerate(row):
            scenic_score = scenic((j, i))
            best_score = max(best_score, scenic_score)
    return best_score

print("Part 1: ", part1(tree_grid))
print()
print("Part 2: ", part2(tree_grid))

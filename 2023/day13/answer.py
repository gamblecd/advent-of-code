import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import print_grid, get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    
    grids =[]
    grid = []
    index=0
    for row in lines:
        if len(row) == 0:
            grids.append(grid)
            grid = []
            index = 0
        else:
            grid.append([])
            for column in row:
                grid[index].append(column)
            index+=1
    grids.append(grid)
    return grids

def getColumn(grid, column):
    return [row[column] for row in grid]
def getRow(grid, row):
    return grid[row]

def compare(row1, row2):
    for i in range(len(row1)):
        if row1[i] != row2[i]:
            return False
    
    return True

def findMirror(grid, column, finder=getColumn):
    gridLength = len(grid[0]) if finder == getColumn else len(grid)
    if (column >= gridLength):
        return -1
    left_index = column
    right_index =column+1
    isMirror = False;
    while left_index >= 0 and right_index < gridLength:
        left = finder(grid, left_index)
        right = finder(grid, right_index)
        if not compare(left, right):
            isMirror = False
            break
        else:
            isMirror = True
        left_index -= 1
        right_index += 1
    if isMirror:
        return column + 1
    else:
        return findMirror(grid, column+1, finder)

def getGridValue(grid):
    v_mirror = findMirror(grid, 0, getColumn)
    if (v_mirror) < 0:
        h_mirror = findMirror(grid, 0, getRow)
        if h_mirror >-1:
            return h_mirror * 100
    else:
        return v_mirror
def part1(grids):
    count = 0
    for g in grids:
        count += getGridValue(g)
    print("Part 1: ",count)

def part2(lines):
    for line in lines:
        pass
    
    print("Part 2: ",)

part1(prep())
print()
part2(prep())
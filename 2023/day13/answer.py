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
    incorrect = []
    for i in range(len(row1)):
        if row1[i] != row2[i]:
            incorrect.append(i)
    return incorrect



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
        if  len(compare(left, right))!= 0:
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

def findMirror3(grid, column, finder=getColumn):
    isColumn = finder == getColumn
    gridLength = len(grid[0]) if finder == getColumn else len(grid)
    if (column >= gridLength):
        return -1
    left_index = column
    right_index =column+1
    isMirror = False;
    count = 0
    while left_index >= 0 and right_index < gridLength:
        left = finder(grid, left_index)
        right = finder(grid, right_index)
        wrongs = compare(left, right)
        if (len(wrongs) == 1):
            ind = wrongs[0]
            if (isColumn):
                point1 = (left_index, ind)
                point2 = (right_index, ind)
            else:
                point1 = (ind, left_index)
                point2 = (ind,right_index)
            #print(point1, point2)
        count+= len(compare(left, right))
        left_index -= 1
        right_index += 1
    if count == 1:
        return column + 1
    else:
        return findMirror3(grid, column+1, finder)

def findMirror2(grid, column, finder=getColumn, canSwap = True):
    isColumn = finder == getColumn
    gridLength = len(grid[0]) if isColumn else len(grid)
    if (column >= gridLength):
        return -1
    left_index = column
    right_index =column+1
    isMirror = False;
    while left_index >= 0 and right_index < gridLength:
        left = finder(grid, left_index)
        right = finder(grid, right_index)
        wrongs = compare(left, right)
        if  len(wrongs) == 1 and canSwap:
            ind = wrongs[0]
            if (isColumn):
                point1 = (left_index, ind)
                point2 = (right_index, ind)
            else:
                point1 = (ind, left_index)
                point2 = (ind,right_index)
            lGrid = [[j for j in i] for i in grid]
            lGrid[point1[1]][point1[0]] = right[ind]
            rGrid = [[j for j in i] for i in grid]
            rGrid[point2[1]][point2[0]] = left[ind]

            lMirror = findMirror2(lGrid, column, finder, False);
            if lMirror >=0 and findMirror(grid, column, finder) != lMirror:
                #print(point1, column, isColumn)
                #insertAndPrint(lGrid, column+1, isColumn)
                return lMirror;
            rMirror = findMirror2(rGrid, column, finder, False);
            if rMirror >=0 and findMirror(grid, column, finder) != rMirror:
                #print(point2, column, isColumn)
                #insertAndPrint(rGrid, column+1, isColumn)
                return rMirror;

            isMirror = False;
            break
        elif len(wrongs) != 0:
            isMirror = False
            break
        else:
            isMirror = not canSwap
        left_index -= 1
        right_index += 1
    if isMirror:
        return column + 1
    else:
        return findMirror2(grid, column+1, finder, canSwap)
    
def insertAndPrint(grid, column, isColumn):
    if isColumn:
        insertColumn(grid, column)
    else:
        insertRow(grid, column)
    for r in grid:
        print("".join(r))
        pass
def insertColumn(grid, column):
    for row in grid:
        row.insert(column, '|')

def insertRow(grid, index):
    rowLength = len(grid[0])
    row = ['-' for _ in range(rowLength)]
    grid.insert(index, row)
        

def getGridValue(grid):
    v_mirror = findMirror(grid, 0, getColumn)
    if (v_mirror) < 0:
        h_mirror = findMirror(grid, 0, getRow)
        if h_mirror > -1:
            return h_mirror * 100
    else:
        return v_mirror
    
def getGridValue2(grid):
    v_mirror = findMirror2(grid, 0, getColumn)
    h_mirror = findMirror2(grid, 0, getRow)
    print(v_mirror, h_mirror)
    if (v_mirror) < 0:
        if h_mirror > -1:
            print(h_mirror)
            insertAndPrint(grid, h_mirror, False)

            return h_mirror * 100
        else:
            print('Edge')
    else:
        print(v_mirror)
        insertAndPrint(grid, v_mirror, True)
        return v_mirror
    
def part1(grids):
    count = 0
    for g in grids:
        count += getGridValue(g)
    print("Part 1: ",count)

def part2(grids):
    count = 0
    for i, g in enumerate(grids):
        print()
        print(i)
        
        count += getGridValue2(g)
    print("Part 2: ", count)

part1(prep())
print()
part2(prep())
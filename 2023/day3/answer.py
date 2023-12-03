import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = []
    symbols = []
    numbers = []
    for y, line in enumerate(fileinput.input(files=(filename))):
        line_data = line.strip()
        lines.append(line_data)
        number = ''
        for x, i in enumerate(line_data):
            if i.isnumeric():
                if number == '':
                    start_point = (x, y)
                number += i
            else:
                if number != '':
                    end_point = (x-1,y)
                    numbers.append((int(number),(start_point, end_point)))
                    number = ''
                if i != '.':
                    symbols.append((i,(x,y)))
        if number != '':
            end_point = (x,y)
            numbers.append((int(number),(start_point, end_point)))
            number = ''
    return numbers, symbols

def isAdjacent(a, b):
    area = [-1, 0, 1]
    for x in area:
        for y in area:
            #print ((a[0]+x, a[1]+y))
            if (a[0]+x, a[1]+y) == b:
                return b;
    return False

def expand(start, end):
    s = start[0]
    e = end[0]
    y = start[1]
    return [(x,y) for x in range(s, e+1)]

def part1(numbers, symbols):
    count = 0
    for (n, p) in numbers:
        points = expand(p[0], p[1])
        is_part_number = False
        for point in points:
            for _ , s in symbols:
                adjacent = isAdjacent(point, s)
                if adjacent:
                    is_part_number = True
                    break
            if is_part_number:
                break
        
        if is_part_number:
            count += n
    print("Part 1: ",count)

def isGear(point, numbers):
    count = [];
    for v, ps in numbers:
        for p in expand(ps[0], ps[1]):
            if isAdjacent(point, p):
                count.append(v)
                break
        if len(count)> 2:
            return False
    if (len(count) == 2):
        return count
    return False

def part2(numbers, symbols):
    count = 0
    for c,s in symbols:
        if c == '*':
            gears = isGear(s, numbers)
            if gears:
                count += gears[0] * gears[1]
                
    
    print("Part 2: ", count)

part1(*prep());
print()
part2(*prep());
import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    histories = [list(map(int, line.strip().split())) for line in fileinput.input(files=(filename))]
    return histories

def diff(a,b):
    if a >= 0 and b >= 0:
        return abs(a-b)
    elif a < 0 and b < 0:
        return abs(abs(a)-abs(b))
    elif a < 0 and b >= 0:
        return b + abs(a)
    elif a >=0 and b < 0:
        return a + abs(b)
    else:
        return 0

def diff2(a,b):
    return a-b

def difference_row(row):
    new_row = []
    for i in range(1, len(row)):
        new_row.append(row[i] - row[i-1])
    return new_row

def extrapolate(row, previous_row):
    initial = 0 
    next = 0
    if len(row) != 0:
        initial = row[-1]
    if len(previous_row) != 0:
        next = previous_row[-1]
    return row.append(initial + next)
    
def criteria(row):
    leng = len(list(filter(lambda x: x!=0, row)))
    return leng != 0

def exec(histories):
    count = 0
    for history in histories:
        rows = [history]
        row = history
        while criteria(row):
            row = difference_row(row)
            rows.append(row)
        
        rows.reverse()
        previous = rows[0]
        previous.append(0)
        for row in rows[1:]:
            extrapolate(row, previous)
            previous = row
        count += rows[-1][-1]
    return count

def part1(histories):
    print("Part 1: ",exec(histories))

def part2(histories):
    for h in histories:
        h.reverse()
    print("Part 2: ", exec(histories))
part1(prep())
print()
part2(prep())
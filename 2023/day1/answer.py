import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def part1():
    count = 0
    for line in fileinput.input(files=(filename)):
        line_data = line.strip()
        v = ''
        for x in line_data:
            if x.isnumeric():
                v = v+x
        v = v[0]+v[-1]
        count= count + int(v)
    print("Part 1: ", count)
    
def part2():
    numbers = ["one", "two", "three", "four", "five", "six", "seven","eight", "nine"]
    count = 0
    for line in fileinput.input(files=(filename)):
        line_data = line.strip()
        n = ''
        w = ''
        for x in line_data:
            if x.isnumeric():
                n = n+x
                w=''
            else:
                w = w+x
                for val in numbers:
                    if val in w:
                        n = n + str(numbers.index(val) + 1)
                        w = x #the words could overlap, and each number could be considered the 'last'
        
        print(n)
        n = n[0]+n[-1]
        count= count + int(n)
    print("Part 1: ", count)

part1();
print()
part2();

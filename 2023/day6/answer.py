import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    time = []
    distance = []
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    time = list(map(int, lines[0].split()[1:]))
    distance = list(map(int, lines[1].split()[1:]))
    return list(zip(time, distance))

# x(t-x) > distance
# x(t-x)-distance > 0
# -x^2 + tx -distance > 0
# t-x > (distance / x) 
#t > (distance / x)+x

def count_winners(time, distance):
    count = 0;
    for i in range(time):
        if i*(time-i) > distance:
            count +=1
    return count

def part1(races):
    counts = []
    for race in races:
        time, distance = race
        counts.append(count_winners(time, distance))
    print("Part 1: ",functools.reduce(lambda a,b: a*b, counts, 1))

def part2(races):
    time = []
    distance =[]
    for race in races:
        time.append(race[0])
        distance.append(race[1])
    time = int(functools.reduce(lambda a, b: a+b, [str(t) for t in time], ''))
    distance = int(functools.reduce(lambda a, b: a+b, [str(d) for d in distance], ''))
    print(time, distance)
    
    print("Part 2: ",count_winners(time, distance))

part1(prep());
print()
part2(prep());
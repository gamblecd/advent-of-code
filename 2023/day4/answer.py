import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    cards = []
    lines = []
    for line in fileinput.input(files=(filename)):
        line_data = line.strip()
        lines.append(line_data)
        winning_numbers, num_have  = line_data.split(":")[1].strip().split(" | ")
        num_have = list(map(int, num_have.split()))
        winning_numbers = list(map(int, winning_numbers.split()))
        cards.append((winning_numbers, num_have));
    return cards

def score(count):
    return 2**(count-1)

def num_of_matches(winning_numbers, num_have):
    sc = 0
    for n in num_have:
        if n in winning_numbers:
            sc += 1;
    return sc
def part1(lines):
    count = 0
    for winning_numbers, num_have in lines:
        sc = num_of_matches(winning_numbers, num_have)
        if (sc > 0):
            count += score(sc);
    print("Part 1: ",count)

def part2(lines):
    copies = [1 for _ in range(len(lines))]
    curr = 0
    for winning_numbers, num_have in lines:
        sc = num_of_matches(winning_numbers, num_have)
        index = 1
        while sc > 0:
            copies[curr+index] += copies[curr]
            sc-=1
            index+=1
        curr+=1
        
    print("Part 2: ",sum(copies))

part1(prep());
print()
part2(prep());
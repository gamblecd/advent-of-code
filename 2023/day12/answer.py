import fileinput, bisect
import re
import functools 
import os
import sys

non_dot_regex = re.compile('[^\.]')

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    mapping = []
    for line in lines:
        springs, alignments = line.split()
        alignments = tuple([int(x) for x in alignments.split(",")])
        mapping.append((springs, alignments))
    return mapping

@functools.lru_cache(maxsize=None)
def find_matches(s, alignments):
    if len(alignments) == 0:
        return '#' not in s
    elif len(s) < alignments[0]:
        return 0
    if s[0]=="#":
        if len(s) >= alignments[0] and '.' not in s[: alignments[0]] and (len(s) == alignments[0] or s[alignments[0]] != '#'):
            return find_matches(s[alignments[0] + 1 :], alignments[1:])
        else:
            return 0
    elif s[0]==".":
        if m := re.search(non_dot_regex, s):
            return find_matches(s[m.start() :], alignments)
        else:
            # end of string while still having dr
            return 0
    else:
        return find_matches(s[1:], alignments) +  find_matches("#" + s[1:], alignments)
        
def part1(mapping):
    total = 0
    for s, a in mapping:
        total += get_matching_mappings(s,a)
    print("Part 1: ", total)

def get_matching_mappings(s, a):
    return find_matches(s, a)

def part2(mapping):
    count = 0  
    for s, a in mapping:
        long_a = a * 5
        c = "?".join([s] * 5)
        count += get_matching_mappings(c, long_a)
    print("Part 2: ",count)

part1(prep())
print()
part2(prep())
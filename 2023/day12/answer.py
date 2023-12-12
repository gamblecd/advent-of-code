import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    mapping = []
    for line in lines:
        springs, alignments = line.split()
        alignments = [int(x) for x in alignments.split(",")]
        mapping.append((springs, alignments))
    return mapping

def is_match(targets, alignments):
    is_match = True
    if (len(targets) == len(alignments)):
        for i, target in enumerate(targets):
            if len(target) != alignments[i]:
                is_match = False
                break;
    else:
        is_match = False
    return is_match

def could_match(targets, alignments):
    for i in range(len(alignments)+1):
        test = alignments[:i]
        if len(targets) == 0:
            return True            
        if len(targets) == len(test):
            for i, t in enumerate(targets):
                if i == (len(targets)-1):
                    if len(t) > test[i]:
                        return False
                else:
                    if len(t) != test[i]:
                        return False
            return True
    return False

def potential_mappings_fast(springs, alignments):
    targets = []
    target = ''
    for i, s in enumerate(springs):
        if s == '.':
            if target:
                targets.append(target)
                # if not could_match(target, alignments):
                #     return False
                target = ''
            # skipp
        if s == '#':
            target += s

    if target:
        targets.append(target)
    return could_match(targets, alignments)


def potential_mappings(springs, alignments):
    count = 0
    targets = []
    target = ''
    for i, s in enumerate(springs):
        if s == '.':
            if target:
                targets.append(target)
                target = ''
            # skipp
        if s == '#':
            target += s

    if target:
        targets.append(target)
    is_match = True
    if (len(targets) == len(alignments)):
        for i, target in enumerate(targets):
            if len(target) != alignments[i]:
                is_match = False
    else:
        is_match = False
    if is_match:
        count += 1
    return count 

def part1(mapping):
    total = 0
    for s, a in mapping:
        springs = get_matching_mappings(s,a)
        total += len(springs)
    print("Part 1: ", total)
    
def get_matching_mappings(s, a):
    springs = ['']
    for c in s:
        #print(len(springs))
        if c == '#' or c == '.':
            for i in range(len(springs)):
                spring = springs[i]
                springs[i] = spring +c
        if c == '?':
            new_springs = []
            for spring in springs:
                st1 = spring + "."
                st2 = spring + "#"
                if (potential_mappings_fast(st1, a)):
                    new_springs.append(st1)
                if (potential_mappings_fast(st2, a)):
                    new_springs.append(st2)
            springs = new_springs
    springs = list(filter(lambda sp: potential_mappings(sp, a), springs))
    return springs;

def part2(mapping):
    total = 0
    for s, a in mapping:
        springs = get_matching_mappings(s, a)
        new_matches = get_matching_mappings(s+"?", a)
        new_matches2 = ['']
        if (s[-1] != "#"):
            new_matches2 = get_matching_mappings("?" + s, a)
        v1, v2, v3 = len(new_matches), len(new_matches2), len(springs)
        if (v1== v3):
            total += v3*v2*v2*v2*v2
        elif (v2 == v3): 
            total += v1*v1*v1*v1*v3
        else:
            #print("Edge")
            total += v3*v2*v1*v2*v3
        # print(v1,v2,v3)
        # print(v3*v2*v2*v2*v2)
        # print(v1*v1*v1*v1*v3)
        #print(len(springs))
        #total += len(springs)
    print("Part 2: ",total)

part1(prep())
print()
part2(prep())
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
        


@functools.lru_cache(maxsize=None)
def could_match(s, targets, alignments):
    for i in range(len(alignments)+1):
        test = alignments[:i]
        if (s, tuple(test)) in mappings.keys():
            return mappings[(s, tuple(test))]
        if len(targets) == 0:
            return True            
        if len(targets) == len(test):
            for i, t in enumerate(targets):
                if i == (len(targets)-1):
                    if len(t) > test[i]:
                        mappings[(s, tuple(test))] = False
                        return False
                else:
                    if len(t) != test[i]:
                        mappings[(s, tuple(test))] = False
                        return False
            mappings[(s, tuple(test))] = True
            return True
    return False
mappings = {}
def potential_mappings_fast(springs, alignments):
    if (springs, alignments) in mappings.keys():
        return mappings[(springs,alignments)]
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
    if could_match(s, tuple(targets), alignments):
        mappings[(springs,alignments)] = True
        return True
    else:
        mappings[(springs,alignments)] = True
        return False
        
    # for i in range(len(alignments)+1):
    #     test = tuple(alignments[:i])
    #     if (springs, test) in mappings.keys():
    #         return mappings[(springs,test)]
    #     if could_match(targets, test):
    #         mappings[(springs, test)] = True
    #         return True
    #     else:
    #         mappings[(springs, test)] = False
    # mappings[(springs, alignments)] = False
    # return False

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
        total += get_matching_mappings(s,a)
    print("Part 1: ", total)
def get_matching_mappings(s, a):
    return find_matches(s, a)

def part2(mapping):
    indexes = {"v1": ["v1", "v4"], "v2": ["v2","v3"],"v3": ["v1", "v4"], "v4": ["v2","v3"]}
    starts = [["v1"], ["v4"]]
    for i in range(1, 5):
        new_starts = []
        for j in range(len(starts)):
            start = starts[j]
            for v in indexes[start[-1]]:
                copy = start.copy();
                copy.append(v)
                new_starts.append(copy)
        starts = new_starts;
    starts = list(filter(lambda s: s[-1] == 'v2' or s[-1] == 'v4',filter(lambda s: s[0]== 'v1' or s[0] == 'v4', starts)))
    count = 0  
    for s, a in mapping:
        print()
        print(s, a)
        long_a = a * 5
        c = "?".join([s] * 5)
        count += get_matching_mappings(c, long_a)
        # print(len(springs))

        # for spr in springs:
        #     v1 = s+"?"
        #     v2 = "?" + s
        #     v3 = "?" + s + "?"
        #     v4 = s
        #     v1_count = get_matching_mappings(v1, a)
        #     v2_count = get_matching_mappings(v2, a)
        #     v3_count = get_matching_mappings(v3, a)
        #     v4_count = get_matching_mappings(v4, a)
        #     # new_matches = get_matching_mappings(spr+"?", a)
        #     # if (s[0] == "#"):
        #     #     # No extra matches with appends, as the groups will be the wrong size
        #     #     # v1 will never be supported (*1)
        #     #     # this  the equivalent of s  + "."
        #     #     print('No v1')
        #     #     new_matches = [1]
        #     # new_matches2 = get_matching_mappings("?" + spr, a)
        #     # if (s[-1] =="#"):
        #     #     # no matches with prepends as the groups will be the wrong size
        #     #     # this is the equivalent of "." + s
        #     #     print('No v2')
        #     #     new_matches2 = [1]
        #     # new_matches3 = get_matching_mappings("?" + spr + "?", a)
        #     # if (s[-1] =="#" and s[0] =="#"):
        #     #     print('No v3')
        #     #     new_matches3 = [1]
        #     # v1, v2, v3, v4 = len(new_matches), len(new_matches2), len(new_matches3), len(springs)
        #     counts = {'v1': v1,'v2': v2,'v3': v3,'v4': v4}
        # #print(c, long_a)
        # cout = get_matching_mappings(c, long_a)
        # #print(cout[0])
        # count += len(cout)
            # if (v1 == v4):
            #     print("v1 == v4")
            #     print(v4*v2*v2*v2*v2)
            #     total += v4*v2*v2*v2*v2
            # elif (v2 == v4): 
            #     print("v2 == v4")
            #     print(v1*v1*v1*v1*v4)
            #     total += v1*v1*v1*v1*v4
            # else:
            #     print("Edge")
            #     print(v1*v4*v2*v4*v2)
            #     print(v4*v2*v3*v1*v4)
            #     total += v4*v2*v3*v1*v4
            # print();
        #print(len(springs))
        #total += len(springs)
    print("Part 2: ",count)

part1(prep())
print()
part2(prep())
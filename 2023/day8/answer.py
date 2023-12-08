import fileinput, bisect
import functools
import os
import sys
import math

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    search_pattern = lines[0];
    tree = {}
    for line in lines[2:]:
        key, nodes = line.split(" = ")
        left, right = nodes[1:len(nodes)-1].split(", ")
        tree[key] = (left,right)
    return search_pattern, tree

def search(direction, key, tree):
    if (direction == 'R'):
        return tree[key][1]
    else:
        return tree[key][0]

def wander(starting, search_pattern, tree):
    direction_index = 0
    steps = 0
    while starting != 'ZZZ':
        direction = search_pattern[direction_index % len(search_pattern)]
        starting = search(direction, starting, tree)
        direction_index +=1
        steps +=1
    return steps;

def part1(search_pattern, tree):
    starting = 'AAA'
    steps = wander(starting, search_pattern, tree)
    
    print("Part 1: ",steps)

def criteria(watchers):
    return len(list(filter(lambda a: a[-1] != 'Z', watchers))) == 0

def part2(search_pattern, tree):
    starters = []
    
    for k in tree.keys():
        if (k[-1]) == 'A':
            starters.append(k)
    direction_index = 0 
    steps = 0;
    starters_matches = {}
    while not criteria(starters):
        if len(starters_matches) == len(starters):
            break;
        direction = search_pattern[direction_index % len(search_pattern)]
        new_starters = []
        for i, starting in enumerate(starters):
            starting = search(direction, starting, tree)
            new_starters.append(starting)
            if (criteria([starting])):
                if i not in starters_matches.keys():
                    starters_matches[i] = steps+1
        direction_index +=1
        steps +=1
        starters = new_starters

    print("Part 2: ",math.lcm(*list(starters_matches.values())))

part1(*prep());
print()
part2(*prep());
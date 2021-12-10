import fileinput, bisect
import functools
from collections import defaultdict, deque
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day10/inputs/actual.txt"

ast = {'(':')', '[':']','{':'}','<':'>'}
scores = defaultdict(lambda: 0, {')': 3, ']': 57, '}': 1197, '>': 25137})
part2_scores = defaultdict(lambda: 0, {')': 1, ']': 2, '}': 3, '>': 4})

stack = deque();


def parse(line):
    if len(line) == 0:
        return 
    global stack;
    char = line[0]
    if char in ast.keys():
        # Valid entry
        stack.append(char);
        return parse(line[1:])
    else:
        expected = ast[stack.pop()]
        if char == expected:
            return parse(line[1:])
        else:
            return char

s = 0
incomplete_line_scores = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    char = parse(line_data)
    if not char:
        fix = ''
        #incomplete:
        while not len(stack) == 0:
            fix += (ast[stack.pop()])
        score = 0
        for i in fix:
            score *=5
            score += part2_scores[i]
        incomplete_line_scores.append(score)
    else:
        stack.clear()
    s += scores[char]

l = len(incomplete_line_scores)
print("Part 1: ", s)
print()
print("Part 2: ", sorted(incomplete_line_scores)[l//2])

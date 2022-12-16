import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
args = sys.argv[1:]
run_actual = len(args) >= 1 and args[0] == "PROD"
if (run_actual):
    filename = os.path.join(script_dir, "inputs", "actual.txt")
else:
    filename = os.path.join(script_dir, "inputs", "ex.txt")


winner = 6
loser = 0
draw = 3

score = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3
}

comps = {
    'Rock': 'Scissors',
    'Paper': 'Rock',
    'Scissors': 'Paper'
}

def compare(a, b):
    if a is b:
        return draw
    if comps[a] is b:
        return winner
    else:
        return loser


def part2_compare(a, b):
    if a is b:
        return draw
    if comps[a] is not b:
        return winner
    else:
        return loser
    
def part2_lookup(a,b):
    if a =='X':
        return comps[b]
    if a == 'Y':
        return b
    if a == 'Z':
        return comps[comps[b]]


foe = {'A': 'Rock', 'B': 'Paper', 'C':'Scissors'}
me = {'X': 'Rock', 'Y': 'Paper', 'Z': 'Scissors'}
part2_score= {'X': loser, 'Y': draw, 'Z': winner}

total = 0
part2 = 0
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    fthrow, mthrow = line_data.split()
    ft = foe[fthrow]
    total = total + compare(me[mthrow], ft) + score[me[mthrow]]
    
    # TODO Always wins, fix to lookup draw score.
    part2 = part2 + part2_score[mthrow] + score[part2_lookup(mthrow, ft)]
    print(part2)
print("Part 1: ", total)
print()
print("Part 2: ", part2)

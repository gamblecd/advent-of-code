import fileinput, bisect
import functools
import operator
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join(script_dir, '..', '..', 'utils')
sys.path.append(mymodule_dir)


class Monkey:
    def __init__(self, index, inventory=None, operation=None, test=None, false_target=None, true_target=None):
        self.index = index
        self.inventory = inventory
        self.operator = operation
        self.test = test
        self.false_target = false_target
        self.true_target = true_target

from util import timer_func as timer
args = sys.argv[1:]
run_actual = len(args) >= 1 and args[0] == "PROD"
if (run_actual):
    filename = os.path.join(script_dir, "inputs", "actual.txt")
else:
    filename = os.path.join(script_dir, "inputs", "ex.txt")

monkeys = []
ops = {"+": operator.__add__, "-": operator.__sub__, "*": operator.__mul__}

in_iter = fileinput.input(files=(filename))

def parse_test(value):
    return lambda x: x % value == 0

def parse_operation(term, op, term2):
    return lambda x: op(x if term == "old" else int(term), x if term2 == "old" else term2)

with fileinput.input(files=(filename)) as in_iter:
    line = in_iter.next();
    while line:
        curr = Monkey(int(line.split()[1]))
        curr.inventory = [int(x) for x in in_iter.next().split()[2:]]
        curr.operation = parse_operation(line)

    
print("Part 1: ",)
print()
print("Part 2: ",)

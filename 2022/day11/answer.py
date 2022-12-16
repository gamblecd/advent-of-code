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
        self.inspection_count = 0
        
    def __repr__(self):
        return "Monkey " + str(self.index) + ": "
    def __str__(self):
        return self.__repr__()

reducer = 1

from util import timer_func as timer
from util import timer_func_with_args as targs
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
    global reducer
    reducer *= int(value)
    return lambda x: x % int(value) == 0

def parse_operation(term, op, term2):
    oper = lambda x: ops[op](x if term == "old" else int(term), x if term2 == "old" else int(term2))
    return oper

with open(filename, 'r') as in_iter:
    nextline = lambda:in_iter.readline().strip();
    while True:
        line = nextline()
        if not line:
            break
        curr = Monkey(int(line.split()[1][0]))
        curr.inventory = [int(x.strip().strip(",")) for x in nextline().split()[2:]]
        term1, op, term2 = nextline().strip().split("=")[1].strip().split()
        curr.operation = parse_operation(term1, op, term2)
        curr.test = parse_test(nextline().split()[-1])
        curr.true_target = int(nextline().split()[-1])
        curr.false_target = int(nextline().split()[-1])
        monkeys.append(curr)
        try:
            line = nextline()
        except:
            break;
    
def inspection(monkey):
    if len(monkey.inventory) == 0:
        return False
    monkey.inspection_count +=1
    item = monkey.inventory.pop(0)
    item = monkey.operation(item)
    item = item % reducer if item > reducer else item
    if monkey.test(item):
        monkeys[monkey.true_target].inventory.append(item)
    else:
        monkeys[monkey.false_target].inventory.append(item)
    return True

def run_round(monkeys):
    for mon in monkeys:
        run_turn(mon)

def run_turn(monkey):
    while(inspection(monkey)):
        pass

for _ in range(10000):
    run_round(monkeys)

for x in monkeys:
    print(x, x.inspection_count)
ms = sorted(monkeys, key=lambda m:m.inspection_count, reverse=True)

print("Part 1: ",ms[0].inspection_count * ms[1].inspection_count)
print()
print("Part 2: ",)

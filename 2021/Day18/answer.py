import fileinput, bisect
import functools
import copy
import math
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day18/inputs/actual.txt"

class Pair():
    def __init__(self, left, right, parent):
        self.left = left
        self.right = right
        self.parent = parent
    
    def __len__(self):
        return 2
    
    def __repr__(self):
        return "[" + str(self.left)+","+ str(self.right) + "]"
    
    def __getitem__(self, key: str):
        if key == 1:
            return self.right
        elif key == 0:
            return self.left
        
    def __setitem__(self, key: str, value):
        if key == 1:
            self.right = value
        elif key == 0:
            self.left = value

def find_comma_index(st):
    stack = []
    for i in range((len(st))):
        c = st[i]
        if c == "[":
            stack.append(c)
        if c == "]":
            stack.pop()
        if c == "," and len(stack)==0:
            return i

def split_pair(st, parent):
    if not st[0] == "[":
        pairs = st.split(",")
        if len(pairs) == 1:
            return int(st)
        else: 
            return Pair(*[int(x) for x in pairs], parent)
    else:
        split_index = find_comma_index(st[1:])+1
        p = Pair(None, None, parent)
        p[0] = split_pair(st[1:split_index], p)
        p[1] = split_pair(st[split_index+1:-1], p)
        return p

numbers = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    numbers.append(split_pair(line_data, None))
magnitude_count = copy.deepcopy(numbers)
def split_number(number, parent):
    return Pair(number//2, math.ceil(number/2), parent)

def add_pairs(left, right):
    p = Pair(None, None, None)
    p.left, p.right = reduce_pair_entry(left), reduce_pair_entry(right)
    p.left.parent = p
    p.right.parent = p
    pair = reduce_pair_entry(p)
    return pair

def explode_pair(pair):
    l = pair[0]
    r = pair[1]
    # Find the first parent that has a left
    p = pair
    starting = None
    if not p.parent == None:
        while not p.parent == None and p.parent.left == p:
            p = p.parent
        starting = p.parent
        
    if starting:
        updated_pair = starting
        update_index = 1
        if isinstance(updated_pair[0], int):
            update_index = 0
            pl1 = updated_pair[0]
        else:
            updated_pair = updated_pair[0]
            while not isinstance(updated_pair[1], int):
                updated_pair = updated_pair[1]
            update_index = 1
            pl1 = updated_pair[1]
        pl1 += l
        updated_pair[update_index] = pl1
        
    p = pair
    starting = None
    if not p.parent == None:
        while not p.parent == None and p.parent.right == p:
            p = p.parent
        starting = p.parent
    if starting:
        updated_pair = starting
        update_index = 1
        if  isinstance(updated_pair[1], int):
            update_index = 1
            pr1 = updated_pair[1]
        else:
            updated_pair = updated_pair[1]
            while not isinstance(updated_pair[0], int):
                updated_pair = updated_pair[0]
            update_index = 0
            pr1 = updated_pair[0]
        pr1 += r
        updated_pair[update_index] = pr1
    return 0

def reduce_explosions(pair, parent, depth, changed=False):
    if changed:
        return pair, changed
    if isinstance(pair, int):
        return pair, False
    if depth == 4:
        pair = explode_pair(pair)
        return pair, True
    pair[0], changedL = reduce_explosions(pair[0], pair, depth+1, changed)
    if (changedL or changed):
        return pair, True
    pair[1], changedR = reduce_explosions(pair[1], pair, depth+1, changed)
    return pair, changedR or changed
def reduce_split(pair, parent, depth, changed=False):
    if changed:
        return pair, changed
    if isinstance(pair, int):
        if pair >=10:
            pair = split_number(pair, parent)
            return pair, True
        else:
            return pair, False
    pair[0], changedL = reduce_split(pair[0], pair, depth+1, changed)
    if (changedL or changed):
        return pair, True
    pair[1], changedR = reduce_split(pair[1], pair, depth+1, changed)
    return pair, changedR or changed

def reduce_pair_entry(pair):
    actions = reduce_explosions, reduce_split
    any_change = True
    while any_change:
        for action in actions:
            pair, any_change = action(pair, pair.parent, 0)
            if any_change:
                break

    return pair
def sum_pairs(numbers):
    if len(numbers) == 2:
        return add_pairs(numbers[0],numbers[1])
    return sum_pairs([add_pairs(numbers[0],numbers[1]), *numbers[2:]])

#sum = sum_pairs(numbers)
def get_magnitude(pair):
    if isinstance(pair, int):
        return pair
    return 3* get_magnitude(pair.left) + 2*get_magnitude(pair.right)

magnitudes = {}
for x in magnitude_count:
    for y in magnitude_count:
        if x != y:
            x1 = copy.deepcopy(x)
            y1 = copy.deepcopy(y)
            pair = (x,y)
            magnitudes[get_magnitude(add_pairs(x1, y1))] = pair
#print("Part 1: ",get_magnitude(sum))
print()
print("Part 2: ",max(magnitudes.keys()))

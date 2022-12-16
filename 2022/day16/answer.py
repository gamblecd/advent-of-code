import fileinput, bisect
import functools
import os
import sys
import queue
import copy
from collections import defaultdict
script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

class Valve():
    def __init__(self, name, rate, children):
        self.name = name
        self.rate = rate
        self.children_ids = children
        self.is_open = False
        
    def __repr__(self):
        return 'Valve ' +  self.name
    def __str__(self):
        return self.__repr__()
valves = {}
valves_list = []
valve_distances = defaultdict(lambda:{})
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    split = line_data.split()
    name = split[1]
    rate = int(split[4].split("=")[1].strip(";"))
    children = [ x.strip(",") for x in split[9:]]
    valve = Valve(name, rate, children)
    valves[name] = valve
    valves_list.append(valve)


attemptData = {'last_valve': '', 'moves':30, 'process':[],'current_valve':valves_list[0],'flow_rate':0,'open_valves': [],'total':0}
possibleValves = [v.name for v in filter(lambda v: v.rate > 0, valves_list)]

def is_open(attemptData, valve):
    return valve.name in attemptData['open_valves']

def set_initial_distances():
    for v in valves:
        for vc in v.children_ids:
            valve_distances[v.name][valves[vc][name]] = 1

def move_to_valve(attemptData, valve):
    attemptData['last_valve'] = attemptData['current_valve'].name
    attemptData['current_valve'] = valve
    attemptData['process'].append("Move to  " + attemptData['current_valve'].name)
    
def open_valve(attemptData):
    attemptData['current_valve'].is_open = True
    attemptData['flow_rate'] += attemptData['current_valve'].rate
    attemptData['open_valves'].append(attemptData['current_valve'].name)
    attemptData['process'].append("Open " + attemptData['current_valve'].name)
    attemptData['total'] += attemptData['moves'] * attemptData['current_valve'].rate

q = queue.PriorityQueue()

# Find distance from every node to every other node
# Find every combination of 

def path_find(fro, to):
    pass

def execute(attemptData):
    if set(attemptData['open_valves']) == set(possibleValves):
        return attemptData
    if attemptData['moves'] == 0:
        return attemptData
    curr = attemptData['current_valve']
    options = []
        # can only move
    for c in curr.children_ids:
        if len(curr.children_ids) == 1 or not c == attemptData['last_valve']:
            new_attempt = copy.deepcopy(attemptData)
            new_attempt['moves'] = attemptData['moves'] - 1
            move_to_valve(new_attempt, valves[c])
            options.append(execute(new_attempt))

    if curr.rate > 0 and not is_open(attemptData, curr):
        # try opening too    
        attemptData['moves'] -= 1
        open_valve(attemptData)
        options.append(execute(attemptData))
    print([x['total'] for x in options])
    return max(options, key=lambda x: x['total'])
    
ret = execute(attemptData)
print(ret['process'])
print(ret['total'])
print("Part 1: ",)
print()
print("Part 2: ",)
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

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    split = line_data.split()
    name = split[1]
    rate = int(split[4].split("=")[1].strip(";"))
    children = [ x.strip(",") for x in split[9:]]
    valve = Valve(name, rate, children)
    valves[name] = valve
    valves_list.append(valve)

valve_distances = defaultdict(lambda: defaultdict(lambda: (len(valves_list), [])))
possibleValves = [v.name for v in filter(lambda v: v.rate > 0, valves_list)]

q = queue.PriorityQueue()

# Find distance from every node to every other node
# Find every combination of 

def find_path(fro, visited):
    if (q.empty()):
        return
    new_distance, c_name, path = q.get()
    visited.append(c_name)
    curr = valves[c_name]

    #Memo distances
    distance, visits = valve_distances[fro.name][c_name]
    min_distance = min(distance, new_distance)
    valve_distances[fro.name][c_name] = (min_distance, [x for x in path])


    for c in curr.children_ids:
        if not c in visited:
            new_path = path.copy()
            new_path.append(c)
            q.put((min_distance+1,c,  new_path))
    find_path(fro, visited)

def path_find(fro, visited):
    for c in fro.children_ids:
        next = valves[c]
        q.put((1, c, [c]))
    find_path(fro, visited)

@timer
def find_all_distances():
    for name, fro in valves.items():
        path_find(fro, [fro.name])

p = queue.PriorityQueue()


def execute_move(starting, opened, moves, total):
    if len(possibleValves) == len(opened):
        return (total, opened)
    options = []
    for v in set(possibleValves) - set(opened):
        # Find the max potential
        movement = moves - valve_distances[starting.name][v][0]
        if (movement <= 0):
            # If we don't have any movement to open the valve, don't worry about this option.
            continue
        new_opened = [v]
        new_opened.extend(opened)
        potential = (movement-1) * valves[v].rate
        new_total, path = execute_move(
            valves[v], new_opened, movement-1, potential)
        options.append((new_total, path))
    if len(options) == 0:
        return (total, opened)
    chosen = max(options, key=lambda x: x[0])
    return (total + chosen[0], chosen[1])

def execute_move_state(state):
    starting, path, opened, moves, total = state
    starting = valves[path[0]]
    path = path[1:]
    return starting, path, opened, moves, total

def execute_open_state(state):
    starting, path, opened, moves, total = state
        # open the valve
    total += moves * starting.rate
    opened.append(starting.name)
    return (starting, path, opened, moves, total)


def execute_decision(state):
    starting, path, opened, moves, total = state
    states = []
    # Start moving to next place
    for v in set(possibleValves) - set(opened):
        # After opening, split this again
        # TODO split state into reusable pieces that can be shared
        # shared state is opened, total, moves
        # unique state is starting, path
        # new path is determined by shared state
        # opened/ total is determined by unique state
        # moves is global

        # each time someone splits, the state
        path = valve_distances[starting.name][v][1]
        states.append(execute_move_state((starting, path, opened.copy(), moves, total)))
    return states

def execute_turn(unique_one, shared, moves):
    starting, path = unique_one
    opened, total = shared
    state = (starting, path, opened, moves, total)
    states = []
    if len(path) == 0 and (starting.rate) != 0 and starting.name not in opened:
        states.append(execute_open_state(state))
    elif len(path) == 0:
        states.extend(execute_decision(state))
    else:
        states.append(execute_move_state(state))
    return states

def execute_elephant(unique, shared, moves):
    opened, total = shared
    global possibleValves
    if len(possibleValves) == len(opened):
        return [shared]
    if (moves <= 0):
        return [shared]
    unique_states = [[],[]]
    curr = 0
    shared_states = [[],[]]
    
    elephant = unique[0]
    person = unique[1]
        
    estates = execute_turn(elephant, shared, moves-1)
    shared = (estates[2], estates[4])
    pstates = execute_turn(person, shared, moves-1)
    shared = (estates[2], estates[4])
    new_states = []
    if len(estates) == 1 and len(pstates)==1:
        new_states.push((estates, pstates), )
    for st in states:
        s = (st[0], st[1])
        unique_states[curr].append(s)
        shared = (st[2], st[4])
        shared_states[curr].append(shared)
    curr +=1

    unique_states = list(zip(unique_states[0],unique_states[1]))
    new_states = [];
    for i, s in enumerate(unique_states):
        new_states.extend(execute_elephant(s, shared_states[curr-2][i], moves))
    return new_states
def execute_minute(state):
    starting, path, opened, moves, total = state
    #decrement moves
    state = (starting, path, opened, moves-1, total)
    states = []
    global possibleValves
    if len(possibleValves) == len(opened):
        return [state]
    if (moves <= 0):
        return [state]
    states = execute_turn((starting, path), (opened,total), moves-1)

    if len(states)== 0:
        return [state]
    new_states = []
    for s in states:
        new_states.extend(execute_minute(s))
    return new_states

@timer
def execute_moves():
    return execute_move(valves["AA"], [], 30, 0)


@timer
def execute_minutes():
    states = execute_minute((valves["AA"], [], [], 30, 0))
    chosen = max(states, key=lambda x: x[-1])
    return chosen[-1], chosen[2]


@timer
def execute_elephants():
    states = execute_elephant([(valves["AA"], []), (valves["AA"], [])], ([], 0), 26)
    chosen = max(states, key=lambda x: x[-1])
    return chosen[-1], chosen[0]

find_all_distances()   
print(execute_moves())
print(execute_minutes())
print(execute_elephants())
#print("Part 1: ", execute_moves()[0])
print()
print("Part 2: ",)
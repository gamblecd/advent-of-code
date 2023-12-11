import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import print_grid, get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

class Pipe:
    
    def __init__(self, label, location, connections) -> None:
        self.label = label
        self.location = location
        self.connections = connections
        self.distance = None
        pass
    
    def set_distance(self, distance):
        self.distance = distance
    def hasConnection(self, connection):
        return connection in self.connections
    
    def isConnected(self, pipeGraph):
        if len(self.connections) == 0:
            return False;
        for c in self.connections:
            if c:
                if not pipeGraph.get(c).hasConnection(self.location):
                    return False
            else:
                return False    
        return True
    
    def follow_pipe(self, entered):
        return list(filter(lambda x: x!= entered, self.connections))[0]
    
    def __repr__(self) -> str:
        return self.label + ": " + str(self.connections)
    
def constructPipe(label, location):
    x,y = location
    if label == '|':
        connections = [(x,y-1), (x, y+1)]
    elif label == '-':
        connections = [(x-1,y), (x+1,y)]
    elif label == 'L':
        connections = [(x,y-1), (x+1,y)]
    elif label == 'J':
        connections = [(x-1,y), (x,y-1)]
    elif label == '7':
        connections = [(x-1,y), (x,y+1)]
    elif label == 'F':
        connections = [(x+1,y), (x,y+1)]
    elif label == '.':
        connections = []
    elif label == 'I':
        label = '.'
        connections = []
    return Pipe(label, location, connections)

def getDirection(next_location,location, pipeGraph):
    try:
        return pipeGraph[next_location].hasConnection(location)
    except:
        return False;

def find_start(location, pipeGraph):
    x,y = location
    isNorth = getDirection((x,y-1),location, pipeGraph)
    isEast = getDirection((x+1,y),location, pipeGraph)
    isSouth = getDirection((x,y+1),location, pipeGraph)
    isWest = getDirection((x-1,y),location, pipeGraph)
    label = 'S'
    if isNorth and isSouth:
        label = '|'
    elif isEast and isWest:
        label = '-'
    elif isNorth and isEast:
        label = 'L'
    elif isNorth and isWest:
        label = 'J'
    elif isSouth and isEast:
        label = 'F'
    elif isSouth and isWest:
        label = '7'    
    
    return constructPipe(label, location)
    

def prep():
    ground = []
    pipeGraph = {}
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    max_y = len(lines)
    for y, line in enumerate(lines):
        max_x = len(line)
        for x, label in enumerate(line):
            location = (x,y)
            if label == 'S':
                start = location
                continue
            else:
                pipe = constructPipe(label, location)        
                pipeGraph[location] = pipe
    
    start = find_start(start, pipeGraph)
    pipeGraph[start.location] = start
    return pipeGraph, start, (max_x, max_y)

def traverse(current, pipeGraph, distance):
    print(current, distance)
    pipe = pipeGraph[current]
    if (pipe.distance):
        return distance-1
    else:
        pipe.set_distance(distance)
        return max([traverse(c,pipeGraph, distance+1) for c in pipe.connections])

def part1(pipeGraph, start, edges):
    stack = []
    stack.append((start.location, 0))
    max_distance = 0
    while len(stack) != 0:
        curr, distance = stack.pop()
        curr = pipeGraph[curr]
        if not curr.distance:
            curr.set_distance(distance)
            max_distance = max(max_distance, distance)
            stack.extend([(c, distance+1) for c in curr.connections])
    try:
        pass
    except:    
        pass
    print("Part 1: ",max_distance  / 2)
    
def touches_outside(location, outside):
    x,y = location
    return (x,y-1) in outside or (x+1,y) in outside or (x,y+1) in outside or (x-1,y) in outside

def get_adjecents(point, maxes, fil= lambda x:True):
    x,y = point
    adjacents = []
    xmax, ymax = maxes
    if (x+1) < xmax:
        adjacents.append((x+1, y))
    if (y+1) < ymax:
        adjacents.append((x, y+1))
    if (x-1) >= 0:
        adjacents.append((x-1, y))
    if (y-1) >= 0:
        adjacents.append((x, y-1))
    return adjacents

def find_location(location, pipeGraph, inside, outside, full_loop, maxes):
    x,y = location
    max_x, max_y = maxes
    if location in inside:
        return True
    if location in outside:
        return True
    if location in full_loop:
        inside.add(location)
        return True
    elif x <= 0 or x >=max_x-1:
        outside.add(location)
        return True
    elif y <= 0 or y >=max_y-1:
        outside.add(location)
        return True

def path_find(location,pipeGraph, outside, inside, full_loop, maxes):
    for a in get_adjecents(location, maxes):
        if not find_location(a, pipeGraph,  inside, outside, full_loop, maxes):
            outside.add(a)
            path_find(a, pipeGraph, outside, inside, full_loop, maxes)

def squeeze_path_find(location, pipeGraph, outside, inside, full_loop, maxes):
    for a in get_adjecents(location, maxes):
        pipe = pipeGraph[a]
        if pipe.isConnected():
            pass
            # traverse the connection
        else:
            squeeze_path_find(location, pipeGraph, outside, inside, full_loop, maxes)

def isNorthSouthSection(start, end):
    if end.label =='7':
        return start.label == 'L'
    elif end.label == 'J':
        return start.label == 'F'
    return end.label == '|'

def part2(pipeGraph, start, max):
    outside = set()
    inside = set()
    full_loop = [start.location]
    location = start.connections[0]
    while location not in full_loop:
        previous =  full_loop[-1]
        full_loop.append(location)
        location = pipeGraph[location].follow_pipe(previous)
    locations = []
    for y in range(max[1]):
        for x in range(max[0]):
            locations.append((x,y))
            find_location((x,y), pipeGraph, inside, outside, full_loop, max)
    
    
    for y in range(max[1]):
        section_start = None
        section_end = None
        is_outside = True
        last_pipe = pipeGraph[(0,y)]
        in_section = False
        section_length = 0
        total_ns = 0
        for x in range(max[0]):
            location = (x,y)
            pipe = pipeGraph[location]
            tube_pipe = pipe.location in full_loop
            last_pipe_was_tube  = last_pipe.location in full_loop
            same_section = pipe.hasConnection(last_pipe.location)
            in_section =  pipe.hasConnection(last_pipe.location)
            leaving_section = last_pipe_was_tube and section_length > 0 and not last_pipe.hasConnection(pipe.location)
            
            new_section = not same_section and tube_pipe

            if leaving_section:
                section_end = last_pipe
                if isNorthSouthSection(section_start, section_end):
                    is_outside = not is_outside
                    total_ns +=1
                # if (tube_pipe and not same_section):
                #     is_outside = not is_outside
            if (new_section):
                section_start = pipe
                section_length = 1
            elif in_section:
                section_length += 1
            if not tube_pipe and is_outside:
                outside.add((x,y))
            last_pipe = pipe
        print(total_ns)
    # for o in outside.copy():
    #     path_find(o, pipeGraph, outside, inside, full_loop, max)
    potential_insides = list(filter(lambda x: x not in outside and x not in full_loop, locations))
    print_grid((0,0), max, '.', [('O',outside), ('I', potential_insides)])
    # print(max[0] * max[1])
    # print(max[0] * max[1] - (len(outside) + len(full_loop)))
    # print(len(outside))
    # print(len(full_loop))
    print("Part 2: ",max[0] * max[1] - (len(outside) + len(full_loop)))

part1(*prep())
print()
part2(*prep())
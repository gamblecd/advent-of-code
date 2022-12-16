import fileinput, bisect
from collections import defaultdict
import numpy as np
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day19/inputs/ex3.txt"

rotate_x = np.array([[1, 0, 0],
                     [0, 0,-1],
                     [0, 1, 0]])
rotate_y = np.array([[0, 0, 1],
                     [0, 1, 0],
                     [-1,0, 0]])
rotate_z = np.array([[0,-1, 0],
                     [1, 0, 0],
                     [0, 0, 1]])


class Scanner:
    def __init__(self, id):
        self.id = id
        self.orientation = None
        self.location = None
        self.scanners = []
        self.beacons = []
        pass
    
    def __repr__(self):
        return self.id  + ": " + str(self.beacons)
scanners = []
current_scanner = None
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if "---" in line_data:
        current_scanner = Scanner(line_data.split()[2])
        scanners.append(current_scanner)
    elif len(line_data) == 0:
        pass
    else:
        current_scanner.beacons.append(tuple(int(x)for x in line_data.split(",")))
rotations = [('x',rotate_x),('y', rotate_y), ('z',rotate_z)]
possible_vectors = defaultdict(lambda:[])
for b in scanners[0].beacons:
    vector = b
    for name, r in rotations:
        for i in range(4):
            vector = np.matmul(r, vector)
            iv = np.multiply(vector, -1)
            print(vector)
            print(iv)
            print()
            possible_vectors[(name,i,-1)].append(iv)
            possible_vectors[(name,i,1)].append(vector)
for s in scanners[1:]:
    for k, pv in possible_vectors.items():
        count = 0
        for pv2 in possible_vectors.values():
            if np.array_equal(pv, pv2):
                count += 1
        print(count)
        if np.array_equal(s.beacons, pv):
            print(k)

print("Part 1: ",)
print()
print("Part 2: ",)

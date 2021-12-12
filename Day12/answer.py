import fileinput, bisect
import functools
import os
import sys
from typing import DefaultDict

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import print_grid, timer_func as timer
filename = "Day12/inputs/actual.txt"

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
  
    def is_large(self):
        return str(self.name).isupper()
    
    def add_child(self, child):
        self.children.append(child)
        
    def get_children(self):
        return self.children
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return "" + self.name

def find_path(node, current_path, paths):
    current_path.append(node)
    if node.name == 'end':
        paths.append(current_path)
    else:
        for child in node.get_children():
            if not child in current_path or child.is_large():
                new_path = current_path.copy()
                find_path(child, new_path, paths)

def find_path_part2(node, current_path, small, paths):
    current_path.append(node)
    if node.name == 'end':
        paths.append(current_path)
    else:
        for child in node.get_children():
            if child.name == 'start':
                continue
            if  current_path.count(child) < 1 or child.is_large():
                new_path = current_path.copy()
                find_path_part2(child, new_path, small, paths)
            elif current_path.count(child) == 1 and not small:
                new_path = current_path.copy()
                find_path_part2(child, new_path, True, paths)

    
nodes = {}
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    node_names = line_data.split("-")
    for node in node_names:
        if not node in nodes:
            nodes[node] = Node(node)
    
    nodes[node_names[0]].add_child(nodes[node_names[1]])
    nodes[node_names[1]].add_child(nodes[node_names[0]])

paths = []
find_path(nodes['start'], [], paths)
paths_part2 = []
find_path_part2(nodes['start'], [], False, paths_part2)
print("Part 1: ",len(paths))
print()
print("Part 2: ", len(paths_part2))

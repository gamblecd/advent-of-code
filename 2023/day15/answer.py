import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    sequences = []
    for line in lines:
        sequences.extend(line.split(","))
    return sequences

def run_hash(s):
    curr = 0
    for c in s:
        curr += ord(c)
        curr *= 17
        curr = curr % 256
    return curr

def eq(boxes, box, label ,focal):
    lens = (label, focal)
    if not box in boxes.keys():
        boxes[box] = [lens]
    else:
        index =  box_index(boxes[box], label) 
        if box_index(boxes[box], label) <0:
            boxes[box].append(lens)
        else:
            boxes[box][index] = lens

def box_index(box, label):
    for i, lens in enumerate(box):
        if lens[0] == label:
            return i
    return -1

def dash(boxes,box, label):
    if box in boxes.keys():
        b = boxes[box]
        index = box_index(b, label)
        if index > -1:
            del b[index]
        if len(b) == 0:
            del boxes[box]

operations = {
    "=":eq,
    "-": dash      
}

def part1(sequences):
    t = 0
    for s in sequences:
        t += run_hash(s)
    print("Part 1: ",t)

def focusing_power(boxes):
    c = 0
    for n, box in boxes.items():
        for i, lens in enumerate(box):
            power = (1+ int(n)) * (i+1) * lens[1]
            c +=power
    return c
def part2(sequences):
    boxes = {}
    for s in sequences:
        if "-" in s:
            label =  s.split("-")[0]
            hsh = run_hash(label)
            dash(boxes, hsh, label)
        elif "=" in s:
            label, focal =  s.split("=")
            hsh = run_hash(label)
            eq(boxes, hsh, label, int(focal))
    print("Part 2: ",focusing_power(boxes))

part1(prep())
print()
part2(prep())
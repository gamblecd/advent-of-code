import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join(script_dir, '..', '..', 'utils')
sys.path.append(mymodule_dir)

from util import timer_func as timer
args = sys.argv[1:]
run_actual = len(args) >= 1 and args[0] == "PROD"
if (run_actual):
    filename = os.path.join(script_dir, "inputs", "actual.txt")
else:
    filename = os.path.join(script_dir, "inputs", "ex.txt")

boxes = []
instructions = []
box_reading = True

def print_cols(columns):
    for c in columns:
        print(c)


def run_instructions(instructions, columns):
    for i in instructions:
        move = i.split()
        perform_move(int(move[1]), int(move[3]), int(move[5]), columns)
        # print_cols(columns)
    return columns


def run_instructions3001(instructions, columns):
    for i in instructions:
        move = i.split()
        perform_move3001(int(move[1]), int(move[3]), int(move[5]), columns)
        # print_cols(columns)
    return columns

def perform_move(count, fro, to, columns):
    for _ in range(count):
        columns[to-1].append(columns[fro-1].pop())

def perform_move3001(count, fro, to, columns):
    fro_len = len(columns[fro-1])
    columns[to-1] +=columns[fro-1][fro_len-count:fro_len]
    columns[fro-1][fro_len-count:fro_len] = []

def generate_columns(boxes):
    column_ids = boxes[-1].split()
    column_count = len(column_ids)
    iterator = 4

    columns = [[] for _ in range(column_count)]
    
    for row in reversed(boxes[:-1]):
        column = 0
        i = 0
        while i < len(row):
            container = row[i:i+iterator]
            if container.strip():
                columns[column].append(container.strip(" []"))
            i+=iterator
            column+=1
    return columns

for line in fileinput.input(files=(filename)):
    line_data = line.strip("\n")
    if not line_data:
        box_reading = False
        continue;

    if box_reading:
        boxes.append(line_data)
    else:
        instructions.append(line_data)

run_instructions(instructions, generate_columns(boxes));


result = ""
columns = run_instructions(instructions, generate_columns(boxes))
for c in columns:
    result += c[-1]

result2 = ""
columns = run_instructions3001(instructions, generate_columns(boxes))
for c in columns:
    result2 += c[-1]

print("Part 1: ", result)
print()
print("Part 2: ", result2)

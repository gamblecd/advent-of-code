from collections import defaultdict
import fileinput, bisect
import functools
import os
import sys
from typing import DefaultDict

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day8/inputs/actual.txt"

segments = {0: ['a', 'b', 'c', 'e', 'f', 'g'],
            1: ['c', 'f'],
            2: ['a', 'c', 'd', 'e', 'g'],
            3: ['a', 'c', 'd', 'f', 'g'], 
            4: ['b', 'c', 'd', 'f'], 
            5: ['a', 'b', 'd', 'f', 'g'], 
            6: ['a', 'b', 'd', 'e', 'f', 'g'], 
            7: ['a', 'c','f'], 
            8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'], 
            9: ['a', 'b', 'c', 'd', 'f', 'g']}

def _find_easy(line):
    summation = 0
    digits = [1, 4, 7, 8]
    for output in line:
        for digit in digits:
            if len(output) == len(segments[digit]):
                summation += 1
                continue
    return summation

def apply_base_logic(line):
    summation = 0
    round_two = []
    round_three = []
    converted_segments = {}
    digits = [1, 4, 7, 8]
    # Round 1
    for output in line:
        for digit in digits:
            if len(output) == len(segments[digit]):
                converted_segments[digit] = set(output)
                continue;
            round_two.append(output)

    # Round 2
    for output in round_two:
        output_set = set(output)
        if len(output_set) == 6:
            if converted_segments[7].issubset(output_set) and converted_segments[4].issubset(output_set):
                # We have a nine
                converted_segments[9] = output_set
            else:
                # We have a six or 0
                if not converted_segments[1].issubset(output_set):
                    #six
                    converted_segments[6] = output_set
                else:
                    #0
                    converted_segments[0] = output_set
        if len(output_set) == 5:
            if converted_segments[7].issubset(output_set):
                #We have a three that we can store on the first pass
                converted_segments[3] = output_set
                # we have a 5 or 2
            else:
                round_three.append(output)

    #Round 3
    for output in round_three:
        output_set = set(output)
        if len(output_set) == 5:
            if not converted_segments[7].issubset(output_set):
                # we have a 5 or 2
                if 6 in converted_segments:
                    if output_set.issubset(converted_segments[6]):
                        converted_segments[5] = output_set
                        # We have a 5
                    else:
                        # We have a 2
                        converted_segments[2] = output_set
                elif 9 in converted_segments:
                    if len(converted_segments[9].difference(output_set)) == 1:
                        #We have a 5;
                        converted_segments[5] = output_set
                    else:
                        converted_segments[2] = output_set
                        # we have a 2
    return summation, converted_segments

part1 = 0
part2 = 0
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    note, output = line_data.split(" | ")
    line_notes = note.split(" ")
    line_output = output.split(" ")
    solutions = apply_base_logic(line_notes)

    part1 += _find_easy(line_output)

    inv_solutions = {"".join(sorted(v)): k for k, v in solutions[1].items()}
    part2 += int("".join([str(inv_solutions["".join(sorted(output))]) for output in line_output]))



print("Part 1: ", part1)

print()
print("Part 2: ", part2)

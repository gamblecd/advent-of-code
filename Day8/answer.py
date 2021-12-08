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

impossible_segments = ['abdeg',"acdefg", "abcdeg"]

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

outputs = []
notes = []
numbers = []


def part1(outputs):
    digits = [1,4,7,8]
    summation = 0
    for line in outputs:
        for output in line:
            for digit in digits:
                if len(output) == len(segments[digit]):
                    summation += 1
    return summation

def find_easy(line):
    possible_solutions = {}
    converted_segments = {}
    digits = [1, 4, 7, 8]
    for output in line:
        for digit in digits:
            if len(output) == len(segments[digit]):
                # for code in output:
                #     possible_solutions[code] = (segments[digit])
                converted_segments[digit] = set(output)
    return line, possible_solutions, converted_segments


def apply_rules(line, possible_solutions, converted_segments):
    #1
    #ossible_solutions[converted_segments[1]] = 'cf'
    #2
    possible_solutions[
        converted_segments[7].difference(converted_segments[1]).pop()] = 'a'


    return line, possible_solutions, converted_segments


def apply_base_logic(line, possible_solutions, converted_segments):
    for output in line:
        output_set = set(output)
        if len(output_set) == 6:
            if converted_segments[7].issubset(output_set) and converted_segments[4].issubset(output_set):
                # We have a nine
                converted_segments[9] = output_set
                possible_solutions[(output_set-
                    converted_segments[4]-converted_segments[7]).pop()] = 'g'
            else:
                # We have a six or 0
                if not converted_segments[1].issubset(output_set):
                    #six
                    converted_segments[6] = output_set
                    possible_solutions[converted_segments[8].difference(
                        output_set).pop()] = 'c'
                else:
                    #0
                    converted_segments[0] = output_set
                    possible_solutions[converted_segments[8].difference(
                        output_set).pop()] = 'd'
        if len(output_set) == 5:
            if converted_segments[7].issubset(output_set):
                #We have a three
                converted_segments[3] = output_set
                pass  # if we have g solved already, we can check against 7 and g to find d
            else:
                pass
                # we have a 5 or 2

    return line, possible_solutions, converted_segments


def apply_secondary_logic(line, possible_solutions, converted_segments):
    for output in line:
        output_set = set(output)
        if len(output_set) == 5:
            if converted_segments[7].issubset(output_set):
                #We have a three
                converted_segments[3] = output_set
                if 9 in converted_segments:
                    possible_solutions[converted_segments[9].difference(
                        output_set).pop()] = 'b'
            else:
                # we have a 5 or 2
                if 6 in converted_segments:
                    if output_set.issubset(converted_segments[6]):
                        converted_segments[5] = output_set
                        possible_solutions[converted_segments[6].difference(
                            output_set).pop()] = 'e'
                        # We have a 5
                    else:
                        # We have a 2
                        converted_segments[2] = output_set
                        possible_solutions[output_set.difference(
                            converted_segments[6]).pop()] = 'c'
                        possible_solutions[converted_segments[3].difference(
                            output_set).pop()] = 'f'
                elif 9 in converted_segments:
                    if len(converted_segments[9].difference(output_set)) == 1:
                        converted_segments[5] = output_set
                        #We have a 5;
                        possible_solutions[converted_segments[9].difference(
                            output_set).pop()] = 'c'
                    else:
                        converted_segments[2] = output_set
                        # we have a 2
                        if 3 in converted_segments:
                            possible_solutions[converted_segments[3].difference(
                                output_set).pop()] = 'f'
                            possible_solutions[converted_segments[2].difference(
                                converted_segments[3]).pop()]= 'e'
                    pass

    return line, possible_solutions, converted_segments

def apply_reductions(line, possible_solutions, converted_segments):
    
    if len(possible_solutions) == 6:
        possible_solutions[(set('abcdefg') -
                           possible_solutions.keys()).pop()] = (set('abcdefg') - possible_solutions.values()).pop()
    return line, possible_solutions, converted_segments

s = 0
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    note, output = line_data.split(" | ")
    line_notes = note.split(" ")
    line_output = output.split(" ")
    notes.append(line_notes)
    outputs.append(line_output)
    solutions = apply_reductions(*apply_secondary_logic(
        *apply_base_logic(*apply_rules(*find_easy(line_notes)))))[2]

    inv_solutions = {"".join(sorted(v)): k for k, v in solutions.items()}
    s += int("".join([str(inv_solutions["".join(sorted(output))]) for output in line_output]))



print("Part 1: ", part1(outputs))

print()
print("Part 2: ", s)

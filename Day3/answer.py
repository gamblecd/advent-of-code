import fileinput, bisect
from functools import reduce
import os
import sys


script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day3/inputs/actual.txt"

bits = []
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    bits.append(list(map(lambda x: int(x),list(line_data))))
    
def flip(bit):
    if bit == 0:
        return 1
    else:
        return 0

@timer
def gamma_rate(bits_array):
    width = len(bits_array[0])
    gamma_rate_arr = []
    for i in range(width):
        z,o = 0,0
        for j in bits_array:
            if j[i] == 0:
                z += 1
            if j[i] == 1:
                o += 1
        if max(z,o) == z:
            gamma_rate_arr.append(0)
        else:
            gamma_rate_arr.append(1)
    return gamma_rate_arr

#find most common value in current bit in area, limit numbers to that, repeat until list is 1

def reducer(index):
    def checker(reduction, value):
        if value[index] == 1:
            return (reduction[0], reduction[1] + 1)
        else:
            return (reduction[0] + 1, reduction[1])
    return checker


def most_common(xy_arr, index, default):
    x,y = reduce(reducer(index), xy_arr, (0,0))
    if x > y:
        return 0;
    if y > x: 
        return 1
    return default

def rate_helper(l, i, comper):
    if len(l) == 1:
        return l[0]
    else:
        comparator = most_common(l, i, 1);
        return rate_helper(list(filter(lambda x: comper(x[i],comparator), l)), i+1, comper)

@timer
def oxygen_rate(l):
    return rate_helper(l, 0, lambda x,y: x == y)

@timer
def co2_rate(l):
    return rate_helper(l, 0, lambda x,y: not x==y)

def to_dec(x):
    return int("".join(str(x) for x in x), 2)

gamma_rate_data = gamma_rate(bits)
epsilon_rate_data = list(map(flip, gamma_rate_data))
gamma = to_dec(gamma_rate_data)
epsilon = to_dec(epsilon_rate_data)
# print(gamma_rate_data)
# print(epsilon_rate_data)

print("Part 1: ",gamma*epsilon)

o_rate = oxygen_rate(bits)
c2_rate = co2_rate(bits)

o = to_dec(o_rate)
c2 = to_dec(c2_rate)
# print(o_rate, o)
# print(c2_rate, c2)

print("Part 2: ", o*c2)

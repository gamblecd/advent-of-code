import fileinput, bisect
import functools
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
gamma_rate_data = gamma_rate(bits)
epsilon_rate_data = list(map(flip, gamma_rate_data))
gamma = int("".join(str(x) for x in gamma_rate_data), 2)
epsilon = int("".join(str(x) for x in epsilon_rate_data), 2)
print(gamma_rate_data)
print(epsilon_rate_data)

print("Part 1: ",gamma*epsilon)
print()
print("Part 2: ",)

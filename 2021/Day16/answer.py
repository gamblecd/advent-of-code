import fileinput, bisect
from collections import defaultdict
import operator
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day16/inputs/actual.txt"
packets = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    packets.append(line_data)


def get_number_and_last_index(packet):
    bits, index = get_bits_for_number(packet, 6)
    return [{'value':int(combine_bits(bits), 2)}], index

operators = { 0:lambda *args : sum(args), 
              1: lambda *args: functools.reduce(lambda x,y: x*y, args, 1),
              2: min, 
              3: max,
              4: lambda x:x,
              5:lambda x,y:1 if x>y else 0,
              6:lambda x,y:1 if x<y else 0,
              7:lambda x,y:1 if x==y else 0}


def get_operator(packet):
    length_id = packet[6]
    if length_id == '0':
        length = int(packet[7:7+15],2)
        packet, offset = get_packets_for_operator_by_length(packet[22:], length)
        return packet, offset+22
    if length_id == '1':
        count = int(packet[7:7+11], 2)
        packet, offset = get_packets_for_operator_by_count(packet[18:], count)
        return packet, offset +18
    pass


types = defaultdict(lambda: get_operator)
types[4] = get_number_and_last_index


def to_binary(packet):
    s = ''
    for n in packet:
        s += format(int(n, 16), '04b')
    return s

def get_version(packet):
    return int(packet[:3], 2)
def get_type_id(packet):
    return int(packet[3:6], 2)


def get_packets_for_operator_by_count(packet, count):
    numbers = []
    index = 0
    x = 0
    while not x == count:
        subpacket, offset = convert(packet[index:])
        index += offset
        numbers.append(subpacket)
        x += 1
    return numbers, index


def get_packets_for_operator_by_length(packet, length):
    numbers = []
    index = 0
    x = 0
    while index < length:
        subpacket, offset = convert(packet[index:])
        index += offset
        numbers.append(subpacket)
        x += 1
    return numbers, index

def get_bits_for_number(packet, index):
    bits = []
    last = False
    while not last:
        last = int(packet[index]) == 0
        bits.append(packet[index+1:index+5])
        index +=5
    return bits, index

def combine_bits(bits):
    return "".join(bits)

def convert(packet):
    version = get_version(packet)
    type = get_type_id(packet)
    action = types[type]
    body, index = action(packet)
    value = 0
    if len(body) == 1:
        value = body[0]['value']
    else:
        value = operators[type](*[x['value'] for x in body])
    return {'v': version,'t': type, 'a': action, 'body':body, 'value': value}, index

def sum_versions(packet):
    if packet['t'] == 4:
        return packet['v']
    else:
        return packet['v'] + sum(map(sum_versions, packet['body']))


print("Part 1: ", sum_versions(convert(to_binary(packets[0]))[0]))
print()
print("Part 2: ", convert(to_binary(packets[0]))[0]['value'])

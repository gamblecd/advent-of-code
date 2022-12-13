import fileinput, bisect
import functools
import os
import sys
import json

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

packet_groups = []
curr_packets = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if not line_data:
        packet_groups.append((curr_packets[0], curr_packets[1]))
        curr_packets = []
    else:
        curr_index = 0
        packet = json.loads(line_data)
        curr_packets.append(packet)
if not len(curr_packets) == 0:
    packet_groups.append((curr_packets[0], curr_packets[1]))
    
def compare(packet, packet2):
    if type(packet) == int:
        if type(packet2) == int:
            return packet - packet2
        if type(packet2) == list:
            return compare([packet], packet2)
    else:
        if type(packet2) == int:
            return compare(packet, [packet2])
        if type(packet2) == list:
            i = 0
            for i in range(len(packet)):
                if i not in range(len(packet2)):
                    return 1
                v = compare(packet[i], packet2[i])
                if v != 0:
                    return v
            return len(packet) - len(packet2)

s = 0
for i,p in enumerate(packet_groups):
    if compare(p[0], p[1]) <= 0:
        s += i+1;
# packet= packet_groups[0]
# s = compare(packet[0], packet[1])
packets =[p for ps in packet_groups for p in ps]
key_func = functools.cmp_to_key(compare)
packets = sorted(packets, key=key_func)
divider1 = bisect.bisect(
    packets, key_func([[2]]), key=key_func) + 1
divider2 = bisect.bisect(
    packets, key_func([[6]]), key=key_func) + 2

print("Part 1: ",s)
print()
print("Part 2: ",divider1 * divider2)

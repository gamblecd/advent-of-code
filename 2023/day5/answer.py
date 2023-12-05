import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

def prep():
    lines = []
    maps = []
    lines = [l for l in fileinput.input(files=(filename))]
    seeds = lines[0].split()[1:]
    for line in lines[2:]:
        line_data = line.strip()
        if line_data == "":
            maps.append((curr_map, {}));
        else:
            line_data = line_data.split();
            if line_data[1] == "map:":
                curr_map = []
            else: 
                dest, source, ran = line_data
                source_start = int(source)
                ran = int(ran)
                source_end = source_start + ran
                dest_start = int(dest)
                dest_end = dest_start + ran

                curr_map.append((source_start, source_end, dest_start,dest_end));
    maps.append((curr_map, {}))
    return seeds, maps

memo = {}
def lookup_fast(source, maps):
    if source in memo.keys():
        return memo[source];
    curr = source
    for map_vals in maps:
        mem = map_vals[1]
        if curr in mem.keys():
            curr = mem[curr]
        else:
            for map_row in map_vals[0]:
                src_start, src_end, dest, dest_end = map_row
                if src_start <=curr < src_end:
                    new_val = dest + curr-src_start
                    mem[curr] = new_val
                    curr = new_val
                    break;
    memo[source] = curr
    return curr

def part1(seeds, maps):
    print("Part 1: ",min([lookup_fast(int(s), maps) for s in seeds]))


def insert_ranges(l, ranges):
    for r in ranges:
        pass

def part2(seeds, maps):
    l = []
    all_ranges = []
    for j in range(0, len(seeds), 2):
        seed_start = int(seeds[j])
        seed_range = int(seeds[j+1])-1
        seed_end = seed_start + seed_range
        ranges = [(seed_start, seed_end)]
        for i, map_vals in enumerate(maps):
            mapped_ranges =[]
            for map_row in map_vals[0]:
                new_ranges = []
                while len(ranges) > 0:
                    r = ranges.pop();
                    seed_start = r[0]
                    seed_end = r[1]
                        
                    src_start, src_end, dest_start, dest_end = map_row
                    new_dest_start_mid = dest_start + (seed_start-src_start)
                    new_dest_end_mid = dest_start + (seed_end-src_start)

                    if (seed_end < src_start)  or src_end <= seed_start:
                        new_ranges.append((seed_start, seed_end))
                        #if (seed_start, seed_end) not in new_ranges:
                            #new_ranges.append((seed_start, seed_end))
                    elif (src_start <= seed_start < src_end  and seed_end < src_end):
                        mapped_ranges.append((new_dest_start_mid, new_dest_end_mid))
                    elif seed_start < src_start and src_start <= seed_end < src_end:
                        new_ranges.append((seed_start, src_start-1))
                        mapped_ranges.append((dest_start, new_dest_end_mid))
                    elif src_start <= seed_start < seed_end and  src_end <= seed_end:
                        new_ranges.append((src_end, seed_end))
                        mapped_ranges.append((new_dest_start_mid, dest_end-1))
                    elif seed_start < src_start and src_end <= seed_end:
                        new_ranges.extend(((seed_start, src_start-1),(src_end, seed_end)))
                        mapped_ranges.append((dest_start, dest_end-1))
                    else:
                        pass
                
                ranges = new_ranges
            ranges.extend(mapped_ranges)
        print(len(ranges))
        all_ranges.extend(ranges)
#        l.append(min([lookup_fast(j, maps) for j in range(seed_start, seed_start+seed_range)]))
         
    print("Part 2: ",min(all_ranges)[0])

part1(*prep());
print()
part2(*prep());
import fileinput
filename = "Day1/inputs/actual.txt"


depths = []

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    depth = int(line_data)
    depths.append(depth)

def calculate_depths(depths, get_val=lambda x,y:y[x]):
    previous_depth = None
    depth = None
    increasing_count = 0
    for index in range(len(depths)):
        val = get_val(index, depths)
        if not (previous_depth == None or val == None):
            if val > previous_depth:
                increasing_count = increasing_count + 1
        #         print('{depth} (increased)'.format(depth=val))
        #     elif val == previous_depth:
        #         print('{depth} (no change)'.format(depth=val))
        # else:
        #     print('{depth} (N/A - no previous measurement)'.format(depth=val))
        previous_depth = val
    return increasing_count

def add_next_2(index,arr):
    if len(arr)-2 <= index:
        return None
    return arr[index] + arr[index +1] + arr[index+2]

# Find how quickly the depth is increasing 
print("Part 1: ", calculate_depths(depths))
print()
#Using 3 value average to determine depth
print("Part 2: ", calculate_depths(depths, add_next_2))

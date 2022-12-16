import fileinput
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..','..', 'utils' )
sys.path.append( mymodule_dir )

args = sys.argv[1:]
run_actual = len(args) >= 1 and args[0] == "PROD"
if (run_actual):
    filename = os.path.join(script_dir, "inputs", "actual.txt");
else:
    filename = os.path.join(script_dir, "inputs", "ex.txt")
    
    
defaultValue = 0
curr = 0
currIncrement = 1
elves = [defaultValue]
part2TopCount = 3

for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if not line_data:
        curr += currIncrement
        elves.append(defaultValue)
    else:
        elves[curr] = elves[curr] + int(line_data)

print("Part 1: ", max(elves)) # find the max number
print()

# Find the summation of the top 3
calorieSum = 0
for _ in range(part2TopCount):
    calorieSum += elves.pop(elves.index(max(elves)))

print("Part 2: ", calorieSum)

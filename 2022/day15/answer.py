import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file,print_grid, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)
low = 0
if len(sys.argv) == 2:
    high = 4000000
else:
    high = 20

sensors = []
beacons = []
sensorToBeacons = {}

xmin = 0
xmax = 0
ymin = 0
ymax = 0
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    splits = line.split()
    sensorX = splits[2]
    sensorY = splits[3]
    beaconX = splits[-2]
    beaconY = splits[-1]
    sensorX = int(sensorX.split("=")[1].strip(","))
    beaconX = int(beaconX.split("=")[1].strip(","))
    sensorY = int(sensorY.split("=")[1].strip(":"))
    beaconY = int(beaconY.split("=")[1])
    sensor = (sensorX, sensorY)
    beacon = (beaconX, beaconY)
    xmin = min(xmin, sensorX, beaconX)
    xmax = max(xmax, sensorX, beaconX)
    ymin = min(ymin, sensorY, beaconY)
    ymax = max(ymax, sensorY, beaconY)

    sensors.append(sensor)
    beacons.append(beacon)
    sensorToBeacons[sensor] = beacon

def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

sensors = sorted(sensors, key=lambda x: distance(
    x, sensorToBeacons[x]), reverse=True)
max_distance = distance(sensors[0], sensorToBeacons[sensors[0]])
for sensor in sensors:
    ymin = min(ymin,sensor[1]-max_distance)
    ymax = max(ymax,sensor[1]+max_distance)
    xmin = min(ymin,sensor[0]-max_distance)
    xmax = max(xmax,sensor[0]+max_distance)

def get_ranges(sensors, y):
    ranges = []
    for sensor in sensors:
        closest_distance = distance(sensor, sensorToBeacons[sensor])
        left_over_distance = closest_distance - abs(sensor[1]-y)
        if (left_over_distance >= 0):
            ranges.append((sensor[0] - left_over_distance, sensor[0]+left_over_distance))
    return ranges

def filterY(iter, y):
    return list(filter(lambda x: x[1] == y, iter))

def consolidate_ranges(ranges):
    ranges = sorted(ranges)
    if len(ranges) == 0:
        return ranges;
    # [(-2, 2), (0, 16), (1, 3), (4, 14), (4, 16), (4, 22), (6, 22), (8, 24), (12, 16), (13, 21), (16, 24), (16, 24)]
    def reducer(x,y):
        rmin, rmax = x[-1]
        xmin, xmax = y
        if (xmin > rmax):
            x.append(y)
        elif xmax > rmax:
            x[-1] = (rmin, xmax)
        elif xmin == rmax + 1:
            x[-1] = (rmin, xmax)
        else:
            # ignore it because we already have it
            pass
        return x
        #x is a list
    return list(functools.reduce(reducer, ranges[1:], [ranges[0]]))

def run_sums(ranges):
    return sum([x[1]-x[0] for x in ranges])

def execute(y, sensorsTest=sensors):

    ranges = get_ranges(sensorsTest, y)
    ranges = consolidate_ranges(ranges)
    return ranges

@timer
def execute_point(point):
    closestDistance = distance(point, sensorToBeacons[point])
    for y in range(point[1]-closestDistance, point[1]+ closestDistance + 1):
        execute(y, [point])
@timer
def execute_all(low, high):
    for i in range(high, low, -1):
        ranges = execute(i)
        if (len(ranges)==2):
            return (ranges[0][1]+1) * 4000000 + i
        
        
# print_grid((xmin,ymin), (xmax,ymax), ".", [,('S', sensors),('B', beacons)])
print("Part 1: ", run_sums(execute(high // 2)))
print()
print("Part 2: ", execute_all(0, high))



import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file,print_grid, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

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

invalid_points = []
valid_points = []

sensors = sorted(sensors, key=lambda x: distance(
    x, sensorToBeacons[x]), reverse=True)
max_distance = distance(sensors[0], sensorToBeacons[sensors[0]])
for sensor in sensors:
    ymin = min(ymin,sensor[1]-max_distance)
    ymax = max(ymax,sensor[1]+max_distance)
    xmin = min(ymin,sensor[0]-max_distance)
    xmax = max(xmax,sensor[0]+max_distance)

def execute(y):
    targets = [(x,y) for x in range(xmin, xmax)]
    for sensor in sensors:
        for test in targets:
            if (test in beacons or test in sensors or test in invalid_points):
                # ignore existing spots
                continue
            closest_distance = distance(sensor, sensorToBeacons[sensor])
            if distance(sensor, (test)) <= closest_distance:
                # No sensor could be here. mark it and move to the next point
                invalid_points.append(test)
        valid_points.append(test)
        for t in invalid_points:
            if t in targets:
                targets.remove(t)

#execute(10)
execute(2000000)
#print_grid((xmin,ymin), (xmax,ymax), ".", [('#', invalid_points),('S', sensors),('B', beacons)])
print("Part 1: ",len(invalid_points))
print()
print("Part 2: ",)
import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)
args = sys.argv[1:]
if len(args) >= 1 and args[0] == "PROD":
    test_min = 200000000000000
    test_max = 400000000000000
else:
    test_min = 7
    test_max = 27
import numpy as np


def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return (float("inf"), float("inf"))
    return (x / z, y / z)


def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    hailstones = []
    for line in lines:
        position, velocity = line.split(" @ ")
        position = [int(c.strip()) for c in position.split(",")]
        velocity = [int(c.strip()) for c in velocity.split(",")]
        hailstones.append((position, velocity))
    return hailstones


def intersect_stones(stone, stone1):
    p1 = stone[0]
    v1 = stone[1]
    a1 = (p1[0], p1[1])
    a2 = (a1[0] + v1[0], a1[1] + v1[1])
    p2 = stone1[0]
    v2 = stone1[1]
    b1 = (p2[0], p2[1])
    b2 = (b1[0] + v2[0], b1[1] + v2[1])
    return get_intersect(a1, a2, b1, b2)


def get_points(stone):
    p1 = stone[0]
    v1 = stone[1]
    a1 = (p1[0], p1[1])
    a2 = (a1[0] + v1[0], a1[1] + v1[1])
    return a1, a2


def slope(a1, a2):
    x1, y1 = a1
    x2, y2 = a2
    if x1 == x2:
        return float("inf")
    if y2 == y1:
        return 0
    else:
        return (y2 - y1) / (x2 - x1)


def y_intercept(slope, a1):
    x, y = a1
    return y - slope * x


def in_area(min, max, point):
    x, y = point
    return min < x < max and min < y < max


def between(i, j, k):
    return i < j <= k or i > j >= k


def distance(i, j):
    return abs(j - i if i < j else i - j)


def in_future(stone, point):
    xe, ye = time_equations(stone)
    x, y = point
    future = xe(x) > 0 and ye(y) > 0
    # print(f"Future for {stone} : {future}")
    return future
    # a1, a2 = get_points(stone)
    # x, y = point
    # # check x
    # positive_x = stone[1][0] > 0
    # positive_y = stone[1][1] > 0

    # if a2[0] == x or a2[1] == y:
    #     print("BLAH")

    # future_x = between(a1[0], x, a2[0])
    # future_y = between(a1[1], y, a2[1])

    # if not future_x:
    #     d1x = distance(a1[0], x)
    #     d2x = distance(a2[0], x)
    #     future_x = d1x > d2x
    # if not future_y:
    #     d1y = distance(a1[1], y)
    #     d2y = distance(a2[1], y)
    #     future_y = d1y > d2y

    # futuristic = future_x and future_y
    # #print(f"Future for {stone} : {futuristic}")
    # return futuristic


def intercept_stone(s1, s2):
    s1_slopes = slope_int(s1)
    s2_slopes = slope_int(s2)
    x = intercept_slope(s1_slopes[0], s2_slopes[0])
    y = intercept_slope(s1_slopes[1], s2_slopes[1])
    return x, y


def intercept_slope(slopes1, slopes2):
    x = (slopes1[1] - slopes2[1]) / (slopes2[0] - slopes1[0])
    return slopes1[0] * x + slopes1[1]


def slope_int(stone):
    pos = stone[0]
    vel = stone[1]

    x_slope = slope((0, pos[0]), (1, pos[0] + vel[0]))
    xy_int = y_intercept(x_slope, (0, pos[0]))
    y_slope = slope((0, pos[1]), (1, pos[1] + vel[1]))
    yy_int = y_intercept(y_slope, (0, pos[1]))
    return ((x_slope, xy_int), (y_slope, yy_int))


def time_equations(stone):
    pos = stone[0]
    vel = stone[1]

    x_slope = slope((0, pos[0]), (1, pos[0] + vel[0]))
    xy_int = y_intercept(x_slope, (0, pos[0]))
    x_equation = lambda y: (y - xy_int) / x_slope
    y_slope = slope((0, pos[1]), (1, pos[1] + vel[1]))
    yy_int = y_intercept(y_slope, (0, pos[1]))
    y_equation = lambda y: (y - yy_int) / y_slope
    return (x_equation, y_equation)


def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return (float("inf"), float("inf"))
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
    return (x1 + ua * (x2 - x1), y1 + ua * (y2 - y1))


def part1(hailstones):
    count = 0
    count2 = 0
    for i, stone in enumerate(hailstones):
        for stone1 in hailstones[i + 1 :]:
            intersect1 = intersect_stones(stone, stone1)
            xy1, xy2 = get_points(stone)
            xy3, xy4 = get_points(stone1)
            x1 = xy1[0]
            x2 = xy2[0]
            x3 = xy3[0]
            x4 = xy4[0]
            y1 = xy1[1]
            y2 = xy2[1]
            y3 = xy3[1]
            y4 = xy4[1]
            test = intersect(x1, y1, x2, y2, x3, y3, x4, y4)
            # print()
            # print(stone)
            # print(stone1)
            # print(intersect)
            # in_future(stone, intersect)
            # in_future(stone1, intersect)
            x, y = test
            if (
                (x > x1) == (x2 - x1 > 0)
                and (y > y1) == (y2 - y1 > 0)
                and (x > x3) == (x4 - x3 > 0)
                and (y > y3) == (y4 - y3 > 0)
                and in_area(test_min, test_max, test)
            ):
                count2 += 1
            if (
                in_future(stone, test)
                and in_future(stone1, test)
                and in_area(test_min, test_max, test)
            ):
                count += 1
    print("Part 1: ", count, count2)


from sympy import Symbol
from sympy import solve_poly_system


def part2(shards):
    # Part 2 uses SymPy. We set up a system of equations that describes the intersections, and solve it.
    x = Symbol("x")
    y = Symbol("y")
    z = Symbol("z")
    vx = Symbol("vx")
    vy = Symbol("vy")
    vz = Symbol("vz")

    equations = []
    t_syms = []
    # the secret sauce is that once you have three shards to intersect, there's only one valid line
    # so we don't have to set up a huge system of equations that would take forever to solve. Just pick the first three.
    for idx, shard in enumerate(shards[:3]):
        # vx is the velocity of our throw, xv is the velocity of the shard we're trying to hit. Yes, this is a confusing naming convention.
        x0, y0, z0 = shard[0]
        xv, yv, zv = shard[1]
        t = Symbol(
            "t" + str(idx)
        )  # remember that each intersection will have a different time, so it needs its own variable

        # (x + vx*t) is the x-coordinate of our throw, (x0 + xv*t) is the x-coordinate of the shard we're trying to hit.
        # set these equal, and subtract to get x + vx*t - x0 - xv*t = 0
        # similarly for y and z
        eqx = x + vx * t - x0 - xv * t
        eqy = y + vy * t - y0 - yv * t
        eqz = z + vz * t - z0 - zv * t

        equations.append(eqx)
        equations.append(eqy)
        equations.append(eqz)
        t_syms.append(t)

    # To my great shame, I don't really know how this works under the hood.
    result = solve_poly_system(equations, *([x, y, z, vx, vy, vz] + t_syms))
    print(result[0][0] + result[0][1] + result[0][2])  # part 2 answer
    print(
        "Part 2: ",
    )


part1(prep())
print()
part2(prep())


# print(get_intersect((0, 1), (0, 2), (1, 10), (1, 9)))  # parallel  lines
# print(get_intersect((0, 1), (0, 2), (1, 10), (2, 10)))  # vertical and horizontal lines
# print(get_intersect((0, 1), (1, 2), (0, 10), (1, 9)))  # another line for fun

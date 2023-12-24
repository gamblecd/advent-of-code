import fileinput, bisect
import functools
import os
import sys
from collections import defaultdict, deque


script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from util import get_input_file, timer_func as timer, print_grid

filename = get_input_file(sys.argv[1:], script_dir)


def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    bricks = []
    for line in lines:
        bricks.append(
            tuple(tuple([int(c) for c in b.split(",")]) for b in line.split("~"))
        )
    xmax = 0
    ymax = 0
    zmax = 0
    for b in bricks:
        xmax = max(xmax, b[0][0], b[1][0])
        ymax = max(ymax, b[0][1], b[1][1])
        zmax = max(zmax, b[0][2], b[1][2])
    bricks = sorted(bricks, key=lambda b: b[0][2])
    return ((xmax, ymax, zmax), bricks)


def get_xs(b):
    return b[0][0], b[1][0]


def get_ys(b):
    return b[0][1], b[1][1]


def get_zs(b):
    return b[0][2], b[1][2]


def in_brick(b, p):
    xs = get_xs(b)
    ys = get_ys(b)
    zs = get_zs(b)
    return (
        p[0] in range(xs[0], xs[1] + 1)
        and p[1] in range(ys[0], ys[1] + 1)
        and p[2] in range(zs[0], zs[1] + 1)
    )


def hits_brick_or_ground(bricks, brick, z, max_z):
    if z > max_z:
        return None
    bricks = bricks.copy()
    bricks.reverse()
    bs = []
    if z == 0:
        return "ground"
    for x in get_brick_range(0, brick):
        for y in get_brick_range(1, brick):
            p = (x, y, z)
            for b in bricks:
                max_z = max(get_zs(b))
                if max_z < z:
                    continue
                if in_brick(b, p):
                    bs.append(b)
    if bs:
        return bs
    return None


def move_down(brick, z=1):
    p1 = brick[0][0], brick[0][1], brick[0][2] - 1
    p2 = brick[1][0], brick[1][1], brick[1][2] - 1

    return (p1, p2)


def validate_collapse(bricks):
    points = []
    point_map = {}
    for brick in bricks:
        for x in get_brick_range(0, brick):
            for y in get_brick_range(1, brick):
                for z in get_brick_range(2, brick):
                    p = (x, y, z)
                    if p in points:
                        raise IndexError("duplicate_point")
                    points.append(p)
                    point_map[p] = brick
    return point_map


@timer
def collapse(bricks):
    supporters = {"ground": []}
    supporting = {}
    new_bricks = []
    max_z = 0
    for b in bricks:
        print(b)
        z = min(get_zs(b))
        z -= 1
        hit_bricks = hits_brick_or_ground(new_bricks, b, z, max_z)
        while not hit_bricks:
            b = move_down(b)
            z -= 1
            hit_bricks = hits_brick_or_ground(new_bricks, b, z, max_z)
        if hit_bricks:
            max_z = max(max_z, *get_zs(b))
            if type(hit_bricks) == list:
                for brick in hit_bricks:
                    if brick not in supporters.keys():
                        supporters.setdefault(brick, set())
                    supporters[brick].add(b)
                    if b not in supporting.keys():
                        supporting.setdefault(b, set())
                    supporting[b].add(brick)

        new_bricks.append(b)
    return new_bricks, supporters, supporting


names = ["A", "B", "C", "D", "E", "F", "G"]


def get_brick_range(index, brick):
    p1, p2 = brick[0][index], brick[1][index]
    return range(p1, p2 + 1)


def print_xz(maxes, bricks):
    bricks_overlays = []
    for i, b in enumerate(bricks):
        overlay = []

        for x in get_brick_range(0, b):
            for z in get_brick_range(2, b):
                overlay.append((x, z))
        bricks_overlays.append((names[i], overlay))
    print_grid((0, 0), (maxes[0], maxes[2]), ".", bricks_overlays)


def print_yz(maxes, bricks):
    bricks_overlays = []
    for i, b in enumerate(bricks):
        overlay = []
        for x in get_brick_range(1, b):
            for z in get_brick_range(2, b):
                overlay.append((x, z))
        bricks_overlays.append((names[i], overlay))
    print_grid((0, 0), (maxes[1], maxes[2]), ".", bricks_overlays)


def count_supporters(bricks, supports, supportings):
    safe = set()
    count = 0
    # brick_names = {}
    # for b in range(len(bricks)):
    #     brick_names[bricks[b]] = names[b]
    for b in bricks:
        if b in supports.keys():
            supporting = supports[b]
            if b == "ground":
                continue
            if len(supporting) == 0:
                safe.add(b)
                count += 1
            else:
                hasSupport = True
                # if brick its supporting has a second supporter
                for brick in supporting:
                    # print(len(supportings[brick]))
                    if len(supportings[brick]) <= 1:
                        hasSupport = False
                if hasSupport:
                    count += 1
                    safe.add(b)
        else:
            count += 1
            safe.add(b)
    return count, safe


def part1(maxes, bricks):
    bricks, supports, supportings = collapse(bricks)
    print("Part 1: ", count_supporters(bricks, supports, supportings)[0])


def find_impact_rec(b, supports, supportings, missing, visited):
    count = 0
    if b in visited:
        return 0
    visited.add(b)
    if b in supports.keys():
        supporting = supports[b]
        if len(supporting) == 0:
            return 1
        else:
            hasSupport = False
            un_supported_bricks = set()
            # if brick its supporting has a second supporter
            for brick in supporting:
                for b1 in supportings[brick]:
                    if b1 == b or b1 in missing:
                        pass
                    else:
                        hasSupport = True
                if not hasSupport:
                    missing.add(brick)
                    if brick not in visited:
                        un_supported_bricks.add(brick)
            for brick in un_supported_bricks:
                count += find_impact_rec(brick, supports, supportings, missing, visited)
        return count + 1
    else:
        return 0


def bfs(supports, supportings, root):
    count = 0
    removed = set()
    queue = deque([root])
    while queue:
        current = queue.popleft()
        removed.add(current)
        if current in supports.keys():
            for brick in supports[current]:
                if not set(supportings[brick])-removed:
                    count +=1
                    queue.append(brick)
    return count

def part2(maxes, bricks):
    bricks, supports, supportings = collapse(bricks)
    safe = count_supporters(bricks, supports, supportings)[1]
    unsafe = set(bricks) - safe
    counts = [bfs(supports, supportings, b) for b in unsafe]
    print("Part 2: ", sum(counts))


part1(*prep())
print()
part2(*prep())

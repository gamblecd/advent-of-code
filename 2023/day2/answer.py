import fileinput, bisect
from functools import reduce
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

cubes = {'red': 12, 'green':13, 'blue':14}


def prep():
    games = []
    for line in fileinput.input(files=(filename)):
        line_data = line.strip()
        splits = line_data.split(":")
        game = splits[0].strip()
        round = splits[1].strip()
        turns = round.split(";")
        sets = []
        for turn in turns:
            draws = turn.strip().split(",")
            pulls = []
            for draw in draws:
                pull = draw.strip()
                pulls.append(pull)
            sets.append(pulls)
        games.append(sets)
    return games

def testGame(game):
    cubes = {'red': 12, 'green':13, 'blue':14}

    for sets in game:
        for pull in sets:
            count, color = pull.split(" ")
            if (int(count) > cubes[color]):
              return False
    return True
def part1(games):
    total = 0
    for game in games:
        if testGame(game):
            total += (games.index(game) + 1)
        pass
    print("Part 1: ", total)


def testGame2(game):
    cubes = {'red': 0, 'green':0, 'blue':0}
    for sets in game:
        for pull in sets:
            count, color = pull.split(" ")
            if (int(count) > cubes[color]):
              cubes[color] = int(count)
    return cubes

def part2(games):
    total = 0
    for game in games:
        cubes = testGame2(game)
        value = reduce(lambda a, b: a*b,cubes.values())
        total += value
    print("Part 2: ",total)

part1(prep());
print()
part2(prep());
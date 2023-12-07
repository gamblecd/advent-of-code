import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append(os.path.join(script_dir, '..', '..', 'utils'))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)

card_rank = ['2','3', '4', '5', '6','7','8','9','T', 'J', 'Q', 'K', 'A']
card_rank2 = ['J', '2','3', '4', '5', '6','7','8','9','T', 'Q', 'K', 'A']

def prep():
    hands = []
    for line in fileinput.input(files=(filename)):
        line_data = line.strip()
        hand, bid = line_data.split();
        hands.append((hand, int(bid)))
    return hands

def sort_hand(hand):
    hand_map = {}
    for x in hand:
        if x in hand_map.keys():
            hand_map[x] = hand_map[x] + 1
        else:
            hand_map[x] = 1
    return hand_map

def sort_hand_wild(hand):
    hand_map = {}
    wilds = 0
    for x in hand:
        if x =='J':
            wilds += 1
        elif x in hand_map.keys():
            hand_map[x] = hand_map[x] + 1
        else:
            hand_map[x] = 1

    if len(hand_map) == 0:
        hand_map['J'] = wilds;
    elif wilds > 0:
        hand_map = dict(sorted(hand_map.items(), key=lambda item: item[1], reverse=True))
        best_key = list(hand_map.keys())[0]
        hand_map[best_key] += wilds
    return hand_map

def get_type(hand_map):
    key_size = len(hand_map.keys())
    if key_size == 1:
        return 7
    if key_size == 5:
        return 1
    if key_size == 4:
        return 2
    if key_size == 2:
        # could be 4 of a kind, or full house
        card = list(hand_map.keys())[0]
        if (hand_map[card] == 1 or hand_map[card] ==4):
            return 6;
        else:
            return 5
    if key_size == 3:
        # could be 3 of a kind, or 2 pair
        for x in hand_map.keys():
            if hand_map[x] == 3:
                return 4
            if hand_map[x] == 2:
                return 3

def compare(hand_a, hand_b, hand_sorter=sort_hand, card_rank=card_rank):
    type_a = get_type(hand_sorter(hand_a))
    type_b = get_type(hand_sorter(hand_b))
    if (type_a == type_b):
        i = 0
        while hand_a[i] == hand_b[i]:
            i+=1
        return card_rank.index(hand_a[i]) - card_rank.index(hand_b[i])
    else:
        return type_a - type_b
    

def part1(hands):
    hands = sorted(hands, key=functools.cmp_to_key(lambda a,b:compare(a[0], b[0])))
    c = 0
    for i, h in enumerate(hands):
        c += (i+1) * h[1]
    print("Part 1: ",c)

def part2(hands):
    hands = sorted(hands, key=functools.cmp_to_key(lambda a,b:compare(a[0], b[0], hand_sorter=sort_hand_wild, card_rank=card_rank2)))
    c = 0
    for i, h in enumerate(hands):
        c += (i+1) * h[1]
        
    print("Part 2: ",c)

part1(prep());
print()
part2(prep());
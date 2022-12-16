import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day4/inputs/actual.txt"

numbers = None
cards = []
card = None
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if numbers == None:
        numbers = [int(x) for x in line_data.split(",")]
    elif line_data == "":
        if not card == None:
            cards.append(card)
        card = []
    else:
        card.append([[int(x),False] for x in line_data.split()])
cards.append(card)

def check_row(card, row):
    for x in card[row]:
        if not x[1]:
            return False
    return True

def check_column(card, col):
    for x in card:
        if not x[col][1]:
            return False
    return True


def check_card(card, num):
    row, col = None, None
    for r in range(len(card)):
        for c in range(len(card[r])):
            spot = card[r][c]
            if spot[0]== num:
                spot[1] = True
                row,col = r,c
                break
            
    if row is None or col is None:
        return False
    else:
        return check_row(card, row) or check_column(card, col)

def check_card_score(card):
    nums = []
    for x in card:
        nums.extend(list(map(lambda x: x[0], filter(lambda v: not v[1], x))))
    return sum(nums)
def reset():
    for card in cards:
        for row in card:
            for column in row:
                column[1] = False

@timer
def play():
    for n in numbers:
        for card in cards:
            if check_card(card, n):
                return n * check_card_score(card)

@timer
def play2():
    cardList = cards.copy();
    winner = None;
    for n in numbers:
        winners = []
        
        for card in cardList:
            if check_card(card, n):
                winners.append(card)
        cardList = list(filter(lambda card: not card in winners, cardList))
        winners = []
        if len(cardList) == 1:
            winner = cardList[0]
        if len(cardList) == 0:
            return check_card_score(winner) * n

print("Part 1: ", play())
reset();
print()
print("Part 2: ",play2())

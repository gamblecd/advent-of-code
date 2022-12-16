import fileinput, bisect
from textwrap import wrap
from collections import Counter, defaultdict
import functools
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'utils' )
sys.path.append( mymodule_dir )

from util import timer_func as timer
filename = "Day14/inputs/actual.txt"

template = None
x = 0
rules = {}
for line in fileinput.input(files=(filename)):
    line_data = line.strip()
    if x==0:
        template = line_data
        x = 1
    else:
        if not line_data == "":
            x,y = line_data.split(" -> ")
            rules[x] = y


def get_pairs(template):
    pairs = []
    for i in range(len(template)-1):
        pairs.append(template[i:i+2])
    return pairs

def insert(pair):
    return pair[0] + rules[pair]

memo = {}
memo2 = {}
def insert_memo(pair):
    if pair in memo:
        return memo[pair]
    return pair[0] + rules[pair]

def run_step(template):
    s = ""
    for pair in get_pairs(template):
        s += insert(pair)
    return s + template[-1]

def run_step_memo(template):
    s = ""
    for pair in get_pairs(template):
        s += insert_memo(pair)[0:-1]
    return s + template[-1]

def recursive(pair, depth, memo):
    if (depth == 1):
        return pair[0] + rules[pair] + pair[1]
    v = pair[0] + rules[pair] + pair[1]
    ret = recursive(v[0:2], depth-1, memo)[0:-1] + recursive(v[1:3], depth-1,memo)
    memo[v] = (ret, depth)
    return ret


@timer
def run_flat(steps):
    flat_template = template
    for i in range(steps):
        flat_template = run_step(flat_template)
    print(flat_template)
    c = Counter(flat_template)
    counts = c.most_common()
    print(counts)
    print(counts[0][1]-counts[-1][1])

@timer
def run_recursive(steps):
    for k in rules.keys():
        memo[k] = recursive(k, steps, memo2)
    keys = list(memo.keys())
    for m in keys:
        for n in keys:
            memo[m+n] = memo[m][:-1] + memo[n]
    s = template
    s2 = ''
    for i in range(1):
        s2 = ''
        for p in get_pairs(s):
            s2 += memo[p][:-1]
        s2 += s[-1]
        s = s2
    #print(s)
    c = Counter(s2)
    counts = c.most_common()
    
    print(counts)
    print(counts[0][1]-counts[-1][1])
def polymer(template, memo):

    # if template in memo2:
    #     m2 = memo2[template]
    #     if m2[1] == 10:
    #         return m2[0]
    if len(template) == 1:
        return template
    if template in memo:
        return memo[template]
    if template in rules:
        return template[0] + rules[template] + template[1]
    else:
        m = template
        split = len(template) // 2
        ret = polymer(template[:split], memo)[:-1] + polymer(template[split-1:split+1],memo)[:-1]+ polymer(template[split:], memo)
        memo[m] = ret
        return ret
@timer
def run_polymer(steps):
    # Prefetch 
    s = template
    for i in range(steps):
        s = polymer(s, memo)
        pass
    c = Counter(s)
    counts = c.most_common()
    #print(s)
    print(counts)
    return counts[0][1]-counts[-1][1]

@timer
def count_pairs(steps):
    chain = {key:0 for key in rules.keys()}
    grow = {key: 0 for key in rules.keys()}
    elements = defaultdict(lambda:0)
    for n in template:
        elements[n] += 1

    for n in get_pairs(template):
        chain[n] += 1

    for i in range(steps):
        for key, value in chain.items():
            insertion = rules[key]
            elements[insertion] +=value
            v1 = key[0] + insertion
            v2 = insertion + key[1]
            grow[v1] += value
            grow[v2] += value
            grow[key] -= value
        
        for key in chain.keys():
            chain[key] += grow[key]
        grow = {key: 0 for key in rules.keys()}
    # for key, value in chain.items():
    #     elements[key[0]] += value
    #     elements[key[1]] += value
    c = Counter(elements)
    return c.most_common()[0][1] - c.most_common()[-1][1]
    return chain, max(elements) - min(elements)
@timer
def run_polymer_with_prefetch(steps, prefetch):
    # Prefetch
    memo = {}
    for k in rules.keys():
        memo[k] = recursive(k, prefetch, memo2)
    s = polymer(template, memo)
    for i in range(2):
        s = polymer(s, memo)
        pass
    c = Counter(s)
    counts = c.most_common()
    #print(s)
    print(counts)
    return counts[0][1]-counts[-1][1]

print("Part 1: ", count_pairs(10))
print()
print("Part 2: ", count_pairs(20))

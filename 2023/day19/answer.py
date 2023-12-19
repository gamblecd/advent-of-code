import fileinput, bisect
import functools
import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)


class Part:
    def __init__(self, attrs) -> None:
        self.attrs = attrs

    def execute(self, test):
        if "<" in test:
            attr, val = test.split("<")
            return self.attrs[attr] < int(val)
        elif ">" in test:
            attr, val = test.split(">")
            return self.attrs[attr] > int(val)

    def total(self):
        return sum(self.attrs.values())


def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    workflows = {}
    parts = []
    get_parts = False
    for line in lines:
        if len(line) == 0:
            get_parts = True
            continue
        if not get_parts:
            # get workflows
            name, workflow = line[:-1].split("{")
            workflow = workflow
            flows = workflow.split(",")
            li = []
            for flow in flows:
                if ":" not in flow:
                    li.append(("", flow))
                else:
                    test, result = flow.split(":")
                    li.append((test, result))
            workflows[name] = li
        else:
            attrs = line[1:-1].split(",")
            part_attrs = {}
            for attr in attrs:
                n, val = attr.split("=")
                part_attrs[n] = int(val)
            parts.append(Part(part_attrs))
    return workflows, parts


def execute_workflow(wf, name, part):
    ret = None
    tests = wf[name]
    for i in range(len(tests)):
        test, result = tests[i]
        if test:
            if part.execute(test):
                return result
        else:
            return result


def part1(workflows, parts):
    rejects = []
    accepted = []
    for p in parts:
        flow = "in"
        while flow:
            result = execute_workflow(workflows, flow, p)
            flow = None
            if result == "A":
                accepted.append(p)
            elif result == "R":
                rejects.append(p)
            else:
                flow = result
    print("Part 1: ", sum([p.total() for p in accepted]))


def test_in_bounds(state, test):
    if "<" in test:
        attr, val = test.split("<")
        min, max = state[attr]
        return max > int(val)
    elif ">" in test:
        attr, val = test.split(">")
        min, max = state[attr]
        return min < int(val)
    return True


def counts(workflows, state, name):
    flow = workflows[name]
    print(name, state)
    success_states = []
    for test, result in flow:
        if not test_in_bounds(state, test):
            break
        if result != 'R':
            state2 = state.copy()
            if "<" in test:
                attr, val = test.split("<")
                val = int(val)
                orig = state[attr]
                new_state = (orig[0], min(orig[1], val-1))
                if new_state[1] < new_state[0]:
                    # invalid state
                    continue
                state2[attr] = new_state
                state[attr] = (min(orig[1], val), orig[1])
            elif ">" in test:
                attr, val = test.split(">")
                val = int(val)
                orig = state[attr]
                new_state = (max(orig[0], val+1), orig[1])
                if new_state[1] < new_state[0]:
                    # invalid state
                    continue
                state2[attr] = new_state
                state[attr] = (orig[0], max(orig[0], val))
        
            if result == "A":
                print("SUCCESS=>", name, state2)
                success_states.append(state2)
            else:
                success_states.extend(counts(workflows, state2.copy(), result))
        else:
            if "<" in test:
                attr, val = test.split("<")
                val = int(val)
                orig = state[attr]
                new_state = (max(orig[0], val), orig[1])
                if new_state[1] < new_state[0]:
                    # invalid state
                    continue
                state[attr] = new_state
            elif ">" in test:
                attr, val = test.split(">")
                val = int(val)
                orig = state[attr]
                new_state = (orig[0], min(orig[1], val))
                if new_state[1] < new_state[0]:
                    # invalid state
                    continue
                state[attr] = new_state
    return success_states


def part2(workflows, parts):
    ranges = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }
    ranges2 = ranges.copy()
    success_states = counts(workflows, ranges, "in")
    for s in success_states:
        print(s)
    count = 0
    for state in success_states:
        distinct = 1
        for a, v in state.items():
            mi, ma = v
            if ma <= mi:
                distinct = 0
                break
            distinct *= (ma - mi)+1
        count += distinct
    print("Part 2: ", count)


part1(*prep())
print()
part2(*prep())

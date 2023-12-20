import fileinput, bisect
import functools
import os
import sys
import math
from queue import Queue

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "..", "..", "utils"))

from util import get_input_file, timer_func as timer

filename = get_input_file(sys.argv[1:], script_dir)


class Pulse:
    def __init__(self, isHigh, sender, target):
        self.sender = sender
        self.high = isHigh
        self.target = target

    def isHigh(self):
        return self.high

    def isLow(self):
        return not self.high

    def __str__(self):
        return "(" + self.sender + ": " + str(self.high) + ", " + self.target + ")"

    def __repr__(self) -> str:
        return self.__str__()


class Module:
    def __init__(self, name, output):
        self.name = name
        self.output = output

    def __key(self):
        return (self.name, self.output)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Module):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__ + ":(" + self.name + ", " + self.output + ")"


class Broadcaster(Module):
    def __init__(self, name, outputs):
        Module.__init__(self, name, outputs)

    def receive(self, pulse, count):
        return [Pulse(pulse.isHigh(), self.name, output) for output in self.output]


class Final(Module):
    def __init__(self, name, outputs):
        Module.__init__(self, name, outputs)

    def receive(self, pulse):
        return [Pulse(pulse.isHigh(), self.name, output) for output in self.output]


class FlipFlop(Module):
    def __init__(self, name, output):
        self.state = False
        Module.__init__(self, name, output)

    def receive(self, pulse, count):
        if pulse.isLow():
            self.state = not self.state
            return [Pulse(self.state, self.name, output) for output in self.output]


class Conjunction(Module):
    def __init__(self, name, output):
        self.pulses = {}
        self.lcm = 0
        self.pulse_count = 0
        Module.__init__(self, name, output)

    def inputs(self, inputs):
        for input in inputs:
            self.pulses[input] = (Pulse(False, input, self.name), 0)

    def last(self, moduleName):
        return self.pulses[moduleName]

    def receive(self, pulse, count):
        currentPulse = self.pulses[pulse.sender]
        if pulse.isHigh() and currentPulse[1] == 0:
            self.pulses[pulse.sender] = (pulse, count)
        else:
            self.pulses[pulse.sender] = (pulse, currentPulse[1])
        isAllHigh = functools.reduce(
            lambda a, p: a and p[0].isHigh(), self.pulses.values(), True
        )
        isAllNonZero = functools.reduce(
            lambda a, p: a and p[1] > 0, self.pulses.values(), True
        )
        if isAllNonZero:
            self.lcm = math.lcm(*[p[1] for p in self.pulses.values()])
            if self.name == "lv":
                raise TryException(self.lcm)
        return [Pulse(not isAllHigh, self.name, output) for output in self.output]


class TryException(Exception):
    def __init__(self, count):
        self.count = count
        Exception.__init__(self, count)


# class MultiConjunction(Module):
#     def __init__(self, name, output, count):
#         self.count = count
#         self.pulses = {}
#         Module.__init__(self, name, output)

#     def receive(self, pulse):
#         self.pulses[pulse.sender] = pulse
#         isAllHigh = functools.reduce(
#             lambda a, p: a and p.isHigh(), self.pulses.values(), True
#         )
#         return [Pulse(not isAllHigh, self.name, output) for output in self.output]


types = {"%": FlipFlop, "&": Conjunction, "b": Broadcaster}


def prep():
    lines = [line.strip() for line in fileinput.input(files=(filename))]
    modules = {}
    input_types = {}
    for line in lines:
        t = line[0]
        name, outputs = line[1:].split(" -> ")
        outputs = [p.strip() for p in outputs.split(",")]
        for output in outputs:
            input_types.setdefault(output, []).append(name)
        if t == "b":
            name = "b" + name
        modules[name] = types[t](name, outputs)
    for input, count in input_types.items():
        existing = modules[input] if input in modules.keys() else None
        if type(existing) == Conjunction:
            existing.inputs(count)

    return modules


def push_button(modules, count=0, r=lambda p: False):
    high_pulse_count = 0
    low_pulse_count = 0
    q = Queue()
    # button push
    q.put(Pulse(False, "button", "broadcaster"))
    while not q.empty():
        pulse = q.get()
        # print(pulse)
        if pulse.isHigh():
            high_pulse_count += 1
        else:
            low_pulse_count += 1

        if pulse.target in modules.keys():
            module = modules[pulse.target]
            ret = module.receive(pulse, count)
            if ret:
                if type(ret) == list:
                    for p in ret:
                        q.put(p)
                else:
                    q.put(ret)
        else:
            if r(pulse):
                raise TryException(high_pulse_count + low_pulse_count)
    return high_pulse_count, low_pulse_count


def part1(modules):
    button_press_count = 1000
    highCount = 0
    lowCount = 0
    for _ in range(button_press_count):
        high, low = push_button(modules)
        highCount += high
        lowCount += low
    print("Part 1: ", lowCount * highCount)


def part2(modules):
    count = 0
    index = 1
    try:
        while True:
            high, low = push_button(modules, index, lambda p: p.isLow())
            index += 1
    except TryException as e:
        count = e.count
    print("Part 2: ", count)


part1(prep())
print()
part2(prep())

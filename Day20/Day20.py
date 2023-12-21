""" Advent of Code 2023, Day 20
    Day 20: Pulse Propagation
    Author: Chi-Kit Pao
"""

import os
import re
import time


def debug(*args):
    if True:
        print(args)


class Module:
    def __init__(self, name, type_, outputs):
        self.name = name
        self.type = type_
        self.outputs = outputs
        # Flip-Flop: off or on
        self.state = False
        # Conjunction: {name: value}
        self.inputs = dict()
        # Common message queue
        self.queue = None

    def connect(self, other):
        if other.type == "&":
            other.inputs[self.name] = False

    def send(self, target, value):
        self.queue.append((self.name, target, value))
        if value:
            self.counters[1] += 1
        else:
            self.counters[0] += 1

    def react(self, source, value):
        if self.type == "":
            for o in self.outputs:
                self.send(o, value)
        elif self.type == "%":
            if value == False:
                self.state = not self.state
                for o in self.outputs:
                    self.send(o, self.state)
        elif self.type == "&":
            assert source in self.inputs
            self.inputs[source] = value
            out_value = not all(self.inputs.values())
            for o in self.outputs:
                self.send(o, out_value)


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))

    modules = dict()
    for line in lines:
        # Example inputs
        # broadcaster -> pc, sg, qf, gt
        # %kz -> gl, vc
        # &db -> np, gt, zj, ns, hh, rt
        p1, p2 = line.split(" -> ")
        match = re.match(r"(?P<symbol>[%&]?)(?P<name>\w+)", p1)
        groupdict = match.groupdict()
        symbol = groupdict["symbol"]
        name = groupdict["name"]

        if p2.find(", ") == -1:
            outputs = [p2]
        else:
            outputs = p2.split(", ")
        modules[name] = Module(name, symbol, outputs)
    for m in modules.values():
        for o in m.outputs:
            if o in modules:
                m.connect(modules[o])
    return modules


def part1(modules, switch_count):
    counters = [0, 0]
    queue = []

    for d in modules.values():
        d.queue = queue
        d.counters = counters
    broadcaster = modules["broadcaster"]

    for _ in range(switch_count):
        counters[0] += 1
        broadcaster.react("", False)
        while True:
            if len(queue) == 0:
                break
            signal = queue.pop(0)
            if signal[1] in modules:
                modules[signal[1]].react(signal[0], signal[2])
    return counters[0] * counters[1]


def main():
    start_time = time.time()
    modules = parse_input()

    result1 = part1(modules, 1000)
    print(
        "Question 1: Consult your module configuration; determine the number\n"
        " of low pulses and high pulses that would be sent after pushing the\n"
        " button 1000 times, waiting for all pulses to be fully handled\n"
        " after each push of the button. What do you get if you multiply\n"
        " the total number of low pulses sent by the total number of high\n"
        " pulses sent?"
    )
    print(f"Answer: {result1}")

    # result2 = 0
    #print(
    #   "Question 2:Reset all modules to their default states. Waiting for\n"
    #   " all pulses to be fully handled after each button press, what is\n"
    #   " the fewest number of button presses required to deliver a single\n"
    #   " low pulse to the module named rx?"
    #)
    # print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Consult your module configuration; determine the number
#  of low pulses and high pulses that would be sent after pushing the
#  button 1000 times, waiting for all pulses to be fully handled
#  after each push of the button. What do you get if you multiply
#  the total number of low pulses sent by the total number of high
#  pulses sent?
# Answer: 812721756
# Time elapsed: 0.047829627990722656 s

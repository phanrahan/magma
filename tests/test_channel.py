import fault
import random
import pytest
import magma as m
from dataclasses import make_dataclass


channel = make_dataclass("channel", ["data", "ready", "valid"])


class Coroutine:
    def __init__(self):
        for key, value in self.IO.items():
            assert isinstance(value, m.Channel)
            if value.type_.isinput():
                setattr(self, key, channel(0, 0, 0))
            else:
                assert value.type_.isoutput()
                setattr(self, key, channel(0, 0, 0))
        self.main = self.main()
        # Initialize main coroutine
        next(self.main)

    def __call__(self):
        # Set default output values
        for key, value in self.IO.items():
            if value.type_.isoutput():
                getattr(self, key).valid = 0
            else:
                assert value.type_.isinput()
                getattr(self, key).ready = 0
        next(self.main)


class Downsample(Coroutine):
    IO = {"data_in": m.In(m.Channel(m.Bits[16])),
          "data_out": m.Out(m.Channel(m.Bits[16]))}

    def main(self):
        while True:
            for y in range(4):
                for x in range(4):
                    # data = data_in.pop()
                    # Wait until data_in valid, will not yield if it
                    # already is
                    while True:
                        self.data_in.ready = 1
                        if self.data_in.valid:
                            break
                        print("Waiting for data_in valid")
                        yield
                    # data_in is valid
                    print("Received valid, accepting data")
                    data = self.data_in.data
                    # yield  # wait a cycle to complete hand shake
                    # ready is implicitly reset to 0
                    # self.data_in.ready = 0
                    if ((x % 2) == 0) & ((y % 2) == 0):
                        # data_out.push(data)
                        # Wait until data_out is ready, will not yield if it
                        # already is
                        while True:
                            self.data_out.data = data
                            self.data_out.valid = 1
                            if self.data_out.ready:
                                break
                            print("Waiting for data_out ready")
                            yield
                        # data_out is ready
                        print("Received ready, sending data")
                        yield  # wait a cycle to complete hand shake
                    else:
                        yield  # wait a cycle to complete hand shake, drop data


def test_basic():
    print("===== Begin basic test =====")
    print("***** TEST EXPECTS: Should idle waiting for upstream data valid *****")
    downsample = Downsample()
    downsample()
    downsample()
    downsample.data_in.data = 0xDEAD
    downsample.data_in.valid = 1
    print("***** TEST EXPECTS: Should hold for a cycle to accept valid data *****")
    downsample()
    downsample.data_in.valid = 0
    print("***** TEST EXPECTS: Should idle waiting for downstream ready *****")
    downsample()
    downsample()
    downsample.data_out.ready = 1
    print("***** TEST EXPECTS: Should hold for a cycle to send valid data *****")
    downsample()
    assert downsample.data_out.valid
    assert downsample.data_out.data == 0xDEAD
    print("***** TEST EXPECTS: Should idle waiting for upstream data valid *****")
    downsample()
    downsample()
    print("===== End basic test =====")


def test_downsample_logic_pass_through():
    downsample = Downsample()
    inputs = [i for i in range(4 * 4)]
    outputs = []
    for i in inputs:
        downsample.data_in.data = i
        downsample.data_in.valid = 1
        downsample.data_out.ready = 1
        downsample()
        if downsample.data_out.valid:
            outputs.append(downsample.data_out.data)

    expected = []
    for y in range(4):
        for x in range(4):
            if ((x % 2) == 0) & ((y % 2) == 0):
                expected.append(y * 4 + x)

    assert outputs == expected, f"{outputs} != {expected}"


def test_downsample_logic_random_stalls():
    downsample = Downsample()
    inputs = [i for i in range(4 * 4)]
    outputs = []
    for i in inputs:
        downsample.data_in.data = i
        while True:
            downsample.data_in.valid = random.getrandbits(1)
            downsample.data_out.ready = random.getrandbits(1)
            downsample()
            if downsample.data_in.valid:
                break
        downsample.data_in.valid = 0
        if not downsample.data_out.ready:
            while True:
                downsample.data_out.ready = random.getrandbits(1)
                downsample()
                if downsample.data_out.ready:
                    break
        if downsample.data_out.valid:
            outputs.append(downsample.data_out.data)
        downsample.data_out.ready = 0

    expected = []
    for y in range(4):
        for x in range(4):
            if ((x % 2) == 0) & ((y % 2) == 0):
                expected.append(y * 4 + x)

    assert outputs == expected, f"{outputs} != {expected}"


def test_producer_consuemr():
    def Producer():
        for y in range(4):
            for x in range(4):
                downsample.data_in.data = y * 4 + x
                print(f"Produced {y * 4 + x}")
                while True:
                    downsample.data_in.valid = random.getrandbits(1)
                    yield
                    if downsample.data_in.valid and downsample.data_in.ready:
                        break

    def Consumer():
        for y in range(4):
            for x in range(4):
                if ((x % 2) == 0) & ((y % 2) == 0):
                    while True:
                        downsample.data_out.ready = random.getrandbits(1)
                        yield
                        if downsample.data_out.ready and \
                           downsample.data_out.valid:
                            break
                    assert downsample.data_out.data == y * 4 + x
                    print(f"Consumed {y * 4 + x}")

    producer = Producer()
    downsample = Downsample()
    consumer = Consumer()
    producer_finished = consumer_finished = False
    while True:
        if not producer_finished:
            try:
                next(producer)
            except StopIteration:
                producer_finished = True
        downsample()
        if not consumer_finished:
            try:
                next(consumer)
            except StopIteration:
                consumer_finished = True
                break
    assert consumer_finished, (producer_finished, consumer_finished)


"""
def test_channel():
    @m.circuit.coroutine
    def downsample(data_in: m.In(m.Channel(m.Bits[16])),
                   data_out: m.Out(m.Channel(m.Bits[16]))):
        while True:
            for y in range(32):
                for x in range(32):
                    data = data_in.pop()
                    if ((x % m.bits(2, 5)) == 0) & ((y % m.bits(2, 5)) == 0):
                        data_out.push(data)
                    yield

    m.compile("build/downsample", downsample, output="coreir-verilog")
    tester = fault.Tester(downsample, downsample.CLK)
    for data in [0xDEAD, 0xBEEF]:
        tester.poke(downsample.data_in, 0xDE)
        tester.poke(downsample.data_in_valid, 1)
        tester.eval()
        tester.print("data_out=%x data_out_valid=%d", downsample.O0, downsample.O1)
    tester.compile_and_run("verilator", directory="tests/build", skip_compile=True)
"""

from hwtypes import Bit
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
                setattr(self, key, channel(0, Bit(0), Bit(0)))
            else:
                assert value.type_.isoutput()
                setattr(self, key, channel(0, Bit(0), Bit(0)))
        self.main = self.main()
        # Initialize main coroutine
        next(self.main)

    def __call__(self):
        next(self.main)


class Downsample(Coroutine):
    IO = {"data_in": m.In(m.Channel(m.Bits[16])),
          "data_out": m.Out(m.Channel(m.Bits[16]))}

    def main(self):
        while True:
            for y in range(4):
                for x in range(4):
                    if ((x % 2) == 0) & ((y % 2) == 0):
                        self.data_in.ready = 1
                        while ~(self.data_in.valid & self.data_out.ready):
                            print("Waiting for data_in.valid and data_out.ready")
                            yield
                        print("Passing data through")
                        self.data_out.data = self.data_in.data
                        self.data_out.valid = 1
                    else:
                        self.data_in.ready = 1
                        while ~self.data_in.valid:
                            print("Waiting for data_in.valid")
                            yield
                        print("Dropping data")
                    yield
                    self.data_out.valid = 0
                    self.data_in.ready = 0


def test_basic():
    print("===== Begin basic test =====")
    print("***** TEST EXPECTS: Should idle waiting for upstream valid and downstream ready *****")
    downsample = Downsample()
    downsample()
    downsample()
    downsample.data_in.data = 0xDEAD
    downsample.data_in.valid = Bit(1)
    downsample.data_out.ready = Bit(1)
    print("***** TEST EXPECTS: Should pass through valid data *****")
    downsample()
    assert downsample.data_out.valid
    assert downsample.data_in.ready
    assert downsample.data_out.data == 0xDEAD
    downsample.data_in.valid = Bit(0)
    downsample.data_out.ready = Bit(0)
    print("***** TEST EXPECTS: Should idle waiting for upstream valid and downstream ready *****")
    downsample()
    downsample()
    print("***** TEST EXPECTS: Should drop valid data *****")
    downsample.data_in.data = 0xBEEF
    downsample.data_in.valid = Bit(1)
    downsample.data_out.ready = Bit(1)
    downsample()
    assert not downsample.data_out.valid
    assert downsample.data_in.ready
    assert downsample.data_out.data == 0xDEAD
    print("===== End basic test =====")


def test_downsample_logic_pass_through():
    downsample = Downsample()
    inputs = [i for i in range(4 * 4)]
    outputs = []
    for i in inputs:
        downsample.data_in.data = i
        downsample.data_in.valid = Bit(1)
        downsample.data_out.ready = Bit(1)
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
            downsample.data_in.valid = valid = Bit(random.getrandbits(1))
            downsample.data_out.ready = ready = Bit(random.getrandbits(1))
            downsample()
            if downsample.data_in.ready:
                break
        if downsample.data_out.valid:
            outputs.append(downsample.data_out.data)

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
                    downsample.data_in.valid = Bit(random.getrandbits(1))
                    yield
                    if downsample.data_in.valid & downsample.data_in.ready:
                        break

    def Consumer():
        for y in range(4):
            for x in range(4):
                if ((x % 2) == 0) & ((y % 2) == 0):
                    while True:
                        downsample.data_out.ready = Bit(random.getrandbits(1))
                        yield
                        if downsample.data_out.ready & \
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


def test_channel():
    @m.circuit.coroutine
    def downsample(data_in: m.In(m.Channel(m.Bits[16])),
                   data_out: m.Out(m.Channel(m.Bits[16]))):
        while True:
            for y in range(32):
                for x in range(32):
                    if ((x % m.bits(2, 5)) == 0) & ((y % m.bits(2, 5)) == 0):
                        while ~data_in.valid | ~data_out.ready:
                            yield
                        data = data_in.pop(blocking=False)
                        data_out.push(data, blocking=False)
                    else:
                        data_in.pop(blocking=True)
                    yield

    m.compile("build/downsample", downsample, output="coreir-verilog")
    tester = fault.Tester(downsample, downsample.CLK)
    for data in [0xDEAD, 0xBEEF]:
        tester.poke(downsample.data_in, 0xDE)
        tester.poke(downsample.data_in_valid, 1)
        tester.eval()
        tester.print("data_out=%x data_out_valid=%d", downsample.O0, downsample.O1)
    tester.compile_and_run("verilator", directory="tests/build", skip_compile=True)













@m.circuit.coroutine
def downsample(data_in: m.In(m.Channel(m.Bits[16])),
               data_out: m.Out(m.Channel(m.Bits[16]))):
    while True:
        for y in range(32):
            for x in range(32):
                self.data_out.data = self.data_in.data
                self.data_out.valid = ((x % m.bits(2, 5)) == 0) & \
                                      ((y % m.bits(2, 5)) == 0)
                yield

"""
1) only sending downstream valid (e.g. for downsample)
2) sending downstream valid and upstream ready, handle upstream valid
   (downstream ready stalls registers) (e.g. for upsample)
"""


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


@m.circuit.coroutine
def downsample(data_in: m.In(m.Channel(m.Bits[16])),
               data_out: m.Out(m.Channel(m.Bits[16]))):
    while True:
        for y in range(32):
            for x in range(32):
                # pop
                self.data_in.ready = 1
                while ~self.data_in.valid:
                    yield
                    # implicitly set ready to 0 after every resume
                    self.data_in.ready = 0
                    self.data_in.ready = 1
                data = self.data_in.data

                if ((x % m.bits(2, 5)) == 0) & ((y % m.bits(2, 5)) == 0):
                    # push
                    self.data_out.valid = 1
                    while ~self.data_out.ready:
                        yield
                        # implicitly set ready to 0 after every resume
                        self.data_in.ready = 0
                # dropping or data_out is ready
                yield
                # implicitly set ready to 0 after every resume
                self.data_in.ready = 0

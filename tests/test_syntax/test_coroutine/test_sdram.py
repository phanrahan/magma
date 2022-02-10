import tempfile
import os
import sys

import magma as m
import fault
from hwtypes import BitVector


def test_sdram():
    CLK_FREQUENCY = 133   # Mhz
    REFRESH_TIME = 32     # ms     (how often we need to refresh)
    REFRESH_COUNT = 8192  # cycles (how many refreshes required per refresh time)

    # clk / refresh =  clk / sec
    #                , sec / refbatch
    #                , ref / refbatch
    CYCLES_BETWEEN_REFRESH = \
        (CLK_FREQUENCY * 1_000 * REFRESH_TIME) // REFRESH_COUNT

    # IDLE = "5'b00000"
    IDLE = BitVector[5](0)

    # INIT_NOP1 = "5'b01000"
    # INIT_PRE1 = "5'b01001"
    # INIT_NOP1_1 = "5'b00101"
    # INIT_REF1 = "5'b01010"
    # INIT_NOP2 = "5'b01011"
    # INIT_REF2 = "5'b01100"
    # INIT_NOP3 = "5'b01101"
    # INIT_LOAD = "5'b01110"
    # INIT_NOP4 = "5'b01111"

    # REF_PRE = "5'b00001"
    # REF_NOP1 = "5'b00010"
    # REF_REF = "5'b00011"
    # REF_NOP2 = "5'b00100"

    # READ_ACT = "5'b10000"
    # READ_NOP1 = "5'b10001"
    # READ_CAS = "5'b10010"
    # READ_NOP2 = "5'b10011"
    # READ_READ = "5'b10100"

    # WRIT_ACT = "5'b11000"
    # WRIT_NOP1 = "5'b11001"
    # WRIT_CAS = "5'b11010"
    # WRIT_NOP2 = "5'b11011"

    INIT_NOP1 = BitVector[5](0b01000)
    INIT_PRE1 = BitVector[5](0b01001)
    INIT_NOP1_1 = BitVector[5](0b00101)
    INIT_REF1 = BitVector[5](0b01010)
    INIT_NOP2 = BitVector[5](0b01011)
    INIT_REF2 = BitVector[5](0b01100)
    INIT_NOP3 = BitVector[5](0b01101)
    INIT_LOAD = BitVector[5](0b01110)
    INIT_NOP4 = BitVector[5](0b01111)

    REF_PRE = BitVector[5](0b00001)
    REF_NOP1 = BitVector[5](0b00010)
    REF_REF = BitVector[5](0b00011)
    REF_NOP2 = BitVector[5](0b00100)

    READ_ACT = BitVector[5](0b10000)
    READ_NOP1 = BitVector[5](0b10001)
    READ_CAS = BitVector[5](0b10010)
    READ_NOP2 = BitVector[5](0b10011)
    READ_READ = BitVector[5](0b10100)

    WRIT_ACT = BitVector[5](0b11000)
    WRIT_NOP1 = BitVector[5](0b11001)
    WRIT_CAS = BitVector[5](0b11010)
    WRIT_NOP2 = BitVector[5](0b11011)

    # CMD_PALL = "8'b10010001"
    # CMD_REF = "8'b10001000"
    # CMD_NOP = "8'b10111000"
    # CMD_MRS = "8'b1000000x"
    # CMD_BACT = "8'b10011xxx"
    # CMD_READ = "8'b10101xx1"
    # CMD_WRIT = "8'b10100xx1"

    CMD_PALL = BitVector[8](0b10010001)
    CMD_REF = BitVector[8](0b10001000)
    CMD_NOP = BitVector[8](0b10111000)
    CMD_MRS = BitVector[8](0b10000000)
    CMD_BACT = BitVector[8](0b10011000)
    CMD_READ = BitVector[8](0b10101001)
    CMD_WRIT = BitVector[8](0b10100001)

    @m.coroutine(manual_encoding=True, reset_type=m.AsyncResetN)
    class SDRAMController:
        def __init__(self):
            self.yield_state = m.Register(T=m.Bits[5], init=INIT_NOP1)()
            self.command = m.Register(T=m.Bits[8], init=CMD_NOP)()
            self.i = m.Register(T=m.UInt[4], init=m.uint(15, 4))()

        def __call__(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
            yield from self.init()
            while True:
                self.command = CMD_NOP
                self.yield_state = IDLE
                yield self.yield_state.prev(), self.command.prev()
                if refresh_cnt >= CYCLES_BETWEEN_REFRESH:
                    yield from self.refresh()
                elif wr_enable:
                    yield from self.write()
                elif rd_enable:
                    yield from self.read()

        def init(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
            # TODO: Desugar for loops
            # for _ in range(15, -1, -1):
            # Loop started by self.i init value
            while True:
                self.command = CMD_NOP
                self.yield_state = INIT_NOP1
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            self.command = CMD_PALL
            self.yield_state = INIT_PRE1
            yield self.yield_state.prev(), self.command.prev()
            self.command = CMD_NOP
            self.yield_state = INIT_NOP1_1
            yield self.yield_state.prev(), self.command.prev()
            self.command = CMD_REF
            self.yield_state = INIT_REF1
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(7, -1, -1):
            self.i = 7
            while True:
                self.command = CMD_NOP
                self.yield_state = INIT_NOP2
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            self.command = CMD_REF
            self.yield_state = INIT_REF2
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(7, -1, -1):
            self.i = 7
            while True:
                self.command = CMD_NOP
                self.yield_state = INIT_NOP3
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            self.command = CMD_MRS
            self.yield_state = INIT_LOAD
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(1, -1, -1):
            self.i = 1
            while True:
                self.command = CMD_NOP
                self.yield_state = INIT_NOP4
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            return refresh_cnt, rd_enable, wr_enable

        def refresh(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
            self.command = CMD_PALL
            self.yield_state = REF_PRE
            yield self.yield_state.prev(), self.command.prev()
            self.command = CMD_NOP
            self.yield_state = REF_NOP1
            yield self.yield_state.prev(), self.command.prev()
            self.command = CMD_REF
            self.yield_state = REF_REF
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(7, -1, -1):
            self.i = 7
            while True:
                self.command = CMD_NOP
                self.yield_state = REF_NOP2
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            return refresh_cnt, rd_enable, wr_enable

        def write(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
            self.command = CMD_BACT
            self.yield_state = WRIT_ACT
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(1, -1, -1):
            self.i = 1
            while True:
                self.command = CMD_NOP
                self.yield_state = WRIT_NOP1
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            self.command = CMD_WRIT
            self.yield_state = WRIT_CAS
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(1, -1, -1):
            self.i = 1
            while True:
                self.command = CMD_NOP
                self.yield_state = WRIT_NOP2
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            return refresh_cnt, rd_enable, wr_enable

        def read(self, refresh_cnt: m.UInt[10], rd_enable: m.Bit, wr_enable: m.Bit) -> (m.Bits[5], m.Bits[8]):
            self.command = CMD_BACT
            self.yield_state = READ_ACT
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(1, -1, -1):
            self.i = 1
            while True:
                self.command = CMD_NOP
                self.yield_state = READ_NOP1
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            self.command = CMD_READ
            self.yield_state = READ_CAS
            yield self.yield_state.prev(), self.command.prev()
            # for _ in range(1, -1, -1):
            self.i = 1
            while True:
                self.command = CMD_NOP
                self.yield_state = READ_NOP2
                yield self.yield_state.prev(), self.command.prev()
                if self.i == 0:
                    break
                self.i = self.i - 1
            self.command = CMD_NOP
            self.yield_state = READ_READ
            yield self.yield_state.prev(), self.command.prev()
            return refresh_cnt, rd_enable, wr_enable


    m.compile("build/SDRAMController", SDRAMController, inline=True)

    tester = fault.Tester(SDRAMController, SDRAMController.CLK)
    tester.circuit.ASYNCRESETN = 1
    tester.eval()
    tester.circuit.ASYNCRESETN = 0
    tester.eval()
    tester.circuit.ASYNCRESETN = 1
    tester.eval()
    for i in range(16):
        tester.circuit.O0.expect(0b01000)
        tester.circuit.O1.expect(0b10111000)
        tester.step(2)
    tester.circuit.O0.expect(0b01001)
    tester.circuit.O1.expect(0b10010001)
    tester.step(2)
    tester.circuit.O0.expect(0b00101)
    tester.circuit.O1.expect(0b10111000)
    tester.step(2)
    tester.circuit.O0.expect(0b01010)
    tester.circuit.O1.expect(0b10001000)
    tester.step(2)

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run("verilator", directory=directory,
                           flags=['-Wno-fatal', "--trace"], skip_compile=True)

import tempfile
import os
import sys

import magma as m
import fault

TEST_SYNTAX_PATH = os.path.join(os.path.dirname(__file__), '../')

sys.path.append(TEST_SYNTAX_PATH)

from test_sequential import DefineRegister


def test_jtag():
    TEST_LOGIC_RESET = m.bits(15, 4)
    RUN_TEST_IDLE = m.bits(12, 4)
    SELECT_DR_SCAN = m.bits(7, 4)
    CAPTURE_DR = m.bits(6, 4)
    SHIFT_DR = m.bits(2, 4)
    EXIT1_DR = m.bits(1, 4)
    PAUSE_DR = m.bits(3, 4)
    EXIT2_DR = m.bits(0, 4)
    UPDATE_DR = m.bits(5, 4)
    SELECT_IR_SCAN = m.bits(4, 4)
    CAPTURE_IR = m.bits(14, 4)
    SHIFT_IR = m.bits(10, 4)
    EXIT1_IR = m.bits(9, 4)
    PAUSE_IR = m.bits(11, 4)
    EXIT2_IR = m.bits(8, 4)
    UPDATE_IR = m.bits(13, 4)

    @m.coroutine2
    class JTAG:
        _manual_encoding_ = True

        def __init__(self):
            self.yield_state = m.Register(
                T=m.Bits[4], init=TEST_LOGIC_RESET, reset_type=m.AsyncReset
            )()

        def __call__(self, tms: m.Bit) -> m.Bits[4]:
            # TODO: Prune infeasible paths (or check if synthesis optimizes
            # them out)
            while True:
                while True:
                    self.yield_state = TEST_LOGIC_RESET
                    yield self.yield_state.prev()
                    if tms == 0:
                        break
                while tms == 0:
                    self.yield_state = RUN_TEST_IDLE
                    yield self.yield_state.prev()
                while tms == 1:
                    self.yield_state = SELECT_DR_SCAN
                    yield self.yield_state.prev()
                    if tms == 0:
                        # dr
                        yield from self.make_scan(CAPTURE_DR, SHIFT_DR,
                                                  EXIT1_DR, PAUSE_DR, EXIT2_DR,
                                                  UPDATE_DR)
                    else:
                        self.yield_state = SELECT_IR_SCAN
                        yield self.yield_state.prev()
                        if tms == 0:
                            # ir
                            yield from self.make_scan(CAPTURE_IR, SHIFT_IR,
                                                      EXIT1_IR, PAUSE_IR,
                                                      EXIT2_IR, UPDATE_IR)
                        else:
                            break

        def make_scan(self, capture, shift, exit_1, pause, exit_2, update):
            def scan(self, tms: m.Bit) -> m.Bits[4]:
                self.yield_state = capture
                yield self.yield_state.prev()
                while True:
                    if tms == 0:
                        while True:
                            self.yield_state = shift
                            yield self.yield_state.prev()
                            if tms != 0:
                                break
                    self.yield_state = exit_1
                    yield self.yield_state.prev()
                    if tms == 0:
                        while True:
                            self.yield_state = pause
                            yield self.yield_state.prev()
                            if tms != 0:
                                break
                        self.yield_state = exit_2
                        yield self.yield_state.prev()
                        if tms != 0:
                            break
                    else:
                        break
                self.yield_state = update
                yield self.yield_state.prev()
                return tms
            return scan()

    m.compile("build/JTAG", JTAG, inline=True)

    tester = fault.Tester(JTAG, JTAG.CLK)
    tester.circuit.tms = 1
    tester.circuit.ASYNCRESET = 0
    tester.eval()
    tester.circuit.ASYNCRESET = 1
    tester.eval()
    tester.circuit.ASYNCRESET = 0
    tester.eval()
    tester.step(2)
    tester.circuit.O.expect(int(TEST_LOGIC_RESET))
    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(TEST_LOGIC_RESET))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(RUN_TEST_IDLE))

    tester.step(2)
    tester.circuit.O.expect(int(RUN_TEST_IDLE))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(SELECT_DR_SCAN))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(CAPTURE_DR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(EXIT1_DR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(PAUSE_DR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(PAUSE_DR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(EXIT2_DR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(SHIFT_DR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(SHIFT_DR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(SHIFT_DR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(EXIT1_DR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(UPDATE_DR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(SELECT_DR_SCAN))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(SELECT_IR_SCAN))

    # BEGIN REPEAT FOR IR
    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(CAPTURE_IR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(EXIT1_IR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(PAUSE_IR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(PAUSE_IR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(EXIT2_IR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(SHIFT_IR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(SHIFT_IR))

    tester.circuit.tms = 0
    tester.step(2)
    tester.circuit.O.expect(int(SHIFT_IR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(EXIT1_IR))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(UPDATE_IR))
    # END REPEAT FOR IR

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(SELECT_DR_SCAN))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(SELECT_IR_SCAN))

    tester.circuit.tms = 1
    tester.step(2)
    tester.circuit.O.expect(int(TEST_LOGIC_RESET))

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-fatal', "--trace"], skip_compile=True)

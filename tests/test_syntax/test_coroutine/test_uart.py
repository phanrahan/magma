import os
import tempfile
import sys

import magma as m
import fault


def test_uart():
    @m.coroutine(reset_type=m.AsyncReset)
    class UART:
        def __init__(self):
            self.message = m.Register(T=m.Bits[8], init=0)()
            self.i = m.Register(T=m.UInt[3], init=7)()
            self.tx = m.Register(T=m.Bit, init=1)()

        def __call__(self, run: m.Bit, message: m.Bits[8]) -> m.Bit:
            while True:
                self.tx = m.bit(1)  # end bit or idle
                yield self.tx.prev()
                if run:
                    self.message = message
                    self.tx = m.bit(0)  # start bit
                    yield self.tx.prev()
                    while True:
                        self.i = self.i - 1
                        self.tx = self.message[self.i.prev()]
                        yield self.tx.prev()
                        if self.i == 7:
                            break

    m.compile("build/UART", UART)

    tester = fault.Tester(UART, UART.CLK)
    tester.poke(UART.CLK, 0)
    tester.poke(UART.ASYNCRESET, 0)
    tester.eval()
    tester.poke(UART.ASYNCRESET, 1)
    tester.eval()
    tester.poke(UART.ASYNCRESET, 0)
    tester.eval()

    # idle
    tester.expect(UART.O, 1)
    tester.print("idle=1\n")

    for message in [0xDE, 0xAD]:
        tester.poke(UART.message, message)
        tester.poke(UART.run, 1)
        tester.step(2)

        # start bit
        tester.print("start=0\n")
        tester.expect(UART.O, 0)
        tester.poke(UART.message, 0xFF)
        tester.poke(UART.run, 0)

        for i in range(8):
            tester.step(2)
            tester.print(f"message[{i}]\n")
            tester.expect(UART.O, (message >> (7-i)) & 1)

        # end bit
        tester.step(2)
        tester.expect(UART.O, 1)

    # idle
    for i in range(2):
        tester.step(2)
        tester.expect(UART.O, 1)

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-fatal', "--trace"], skip_compile=True)

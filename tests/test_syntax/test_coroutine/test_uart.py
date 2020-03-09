import magma as m


def test_uart():
    @m.syntax.coroutine
    class UART:
        def __init__(self):
            self.message: m.Bits[8] = 0
            self.i: m.UInt[3] = 0
            self.tx: m.Bit = 1

        def __call__(self, run: m.Bit, message: m.Bits[8]) -> m.Bit:
            self.tx = m.bit(1)  # end bit or idle
            yield self.tx.prev()
            if run:
                self.message = message
                self.tx = m.bit(0)  # start bit
                yield self.tx.prev()
                while True:
                    self.i = self.i + 1
                    self.tx = self.message[self.i.prev()]
                    yield self.tx.prev()
                    if self.i == 0:
                        break
    m.compile("build/uart", UART)

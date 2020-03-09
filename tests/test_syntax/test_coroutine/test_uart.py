import magma as m


def test_uart():
    @m.syntax.coroutine
    class UART:
        def __init__(self):
            self.message: m.Bits[8] = 0
            self.i: m.Bits[2] = 0
            self.tx: m.Bit = 1

        def __call__(self, run: m.Bit, message: m.Bits[8]) -> m.Bit:
            self.tx = 1  # end bit or idle
            yield self.tx.prev()
            if run:
                self.message = message
                self.tx = 0  # start bit
                yield self.tx.prev()
                while True:
                    self.i += 1
                    self.tx = self.message[self.i.prev()]
                    yield self.tx.prev()
                    if self.i == 0:
                        break
    m.compile("build/uart", UART)

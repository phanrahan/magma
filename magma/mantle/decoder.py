import magma as m


class Decoder(m.Generator2):
    """Decodes n-bit value into a one hot encoding (2^n bits).
    """

    def __init__(self, n: int):
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[2**n]))
        self.io.O @= m.bits(1, 2**n) << m.zext_to(self.io.I, 2**n)


def decode(x: m.Bits) -> m.Bits:
    n = len(x)
    return m.Bits[2**n](1) << m.zext_to(x, 2**n)

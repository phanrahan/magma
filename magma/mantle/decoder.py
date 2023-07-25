import magma as m


class Decoder(m.Generator2):
    """
    Input `n` bits
    Output `2**n` bits one-hot encoding the integer value of `n`
    """

    def __init__(self, n: int):
        self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[2**n]))
        self.io.O @= m.bits(1, 2**n) << m.zext_to(self.io.I, 2**n)


def decode(x: m.Bits):
    n = len(x)
    return m.Bits[2**n](1) << m.zext_to(x, 2**n)

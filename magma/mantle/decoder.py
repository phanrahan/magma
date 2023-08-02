from magma.bits import Bits
from magma.conversions import bits, zext_to
from magma.generator import Generator2
from magma.interface import IO
from magma.t import In, Out


class Decoder(Generator2):
    """Decodes n-bit value into a one hot encoding (2^n bits).
    """

    def __init__(self, n: int):
        self.io = IO(I=In(Bits[n]), O=Out(Bits[2**n]))
        self.io.O @= bits(1, 2**n) << zext_to(self.io.I, 2**n)


def decode(x: Bits) -> Bits:
    n = len(x)
    return Bits[2**n](1) << zext_to(x, 2**n)

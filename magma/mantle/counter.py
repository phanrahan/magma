from typing import Optional

from magma.bit import Bit
from magma.bits import UInt
from magma.clock_io import gen_clock_io
from magma.generator import Generator2
from magma.interface import IO
from magma.mantle.util import ispow2
from magma.primitives.mux import mux
from magma.primitives.register import Register
from magma.t import Type, Out


class Counter(Generator2):
    """Counts to `n` (0 to n - 1) repeatedly.
    """

    def __init__(
        self,
        n: int,
        has_enable: bool = False,
        has_cout: bool = False,
        reset_type: Optional[Type] = None
    ):
        num_bits = max((n - 1).bit_length(), 1)

        self.io = IO(O=Out(UInt[num_bits]))
        if has_cout:
            self.io += IO(COUT=Out(Bit))
        self.io += gen_clock_io(reset_type, has_enable)

        reg = Register(
            UInt[num_bits], has_enable=has_enable, reset_type=reset_type
        )()

        if has_enable:
            reg.CE @= self.io.CE

        self.io.O @= reg.O

        if has_cout:
            COUT = reg.O == (n - 1)
            if has_enable:
                COUT &= self.io.CE
            self.io.COUT @= COUT

        I = reg.O + 1
        if not ispow2(n):
            I = mux([I, 0], reg.O == (n - 1))
        reg.I @= I

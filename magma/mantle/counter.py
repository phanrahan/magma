from typing import Optional

import magma as m
from magma.mantle.util import ispow2


class Counter(m.Generator2):
    """
    Counts `n` times (0 to n - 1)
    """

    def __init__(self, n: int, has_enable: bool = False,
                 has_cout: bool = False, reset_type: Optional[m.Type] = None):
        num_bits = max((n - 1).bit_length(), 1)

        self.io = m.IO(O=m.Out(m.UInt[num_bits]))
        if has_cout:
            self.io += m.IO(COUT=m.Out(m.Bit))
        self.io += m.clock_io.gen_clock_io(reset_type, has_enable)

        reg = m.Register(m.UInt[num_bits], has_enable=has_enable,
                         reset_type=reset_type)()
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
            I = m.mux([I, 0], reg.O == (n - 1))
        reg.I @= I

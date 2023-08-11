"""
Convenience wrappers around SB_LUT4
"""
from magma.bit import Bit
from magma.interface import IO
from magma.generator import Generator2
from magma.mantle.lattice.ice40.plb import SB_LUT4
from magma.t import In, Out


class LUT2(Generator2):
    def __init__(self, contents):
        self.io = IO(
            I0=In(Bit),
            I1=In(Bit),
            O=Out(Bit),
        )
        self.io.O @= SB_LUT4(LUT_INIT=contents)(
            self.io.I0,
            self.io.I1,
            0,
            0
        )


class LUT3(Generator2):
    def __init__(self, contents):
        self.io = IO(
            I0=In(Bit),
            I1=In(Bit),
            I2=In(Bit),
            O=Out(Bit),
        )
        self.io.O @= SB_LUT4(LUT_INIT=contents)(
            self.io.I0,
            self.io.I1,
            self.io.I2,
            0
        )

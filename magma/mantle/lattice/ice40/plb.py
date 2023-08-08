import hwtypes as ht

from magma.bit import Bit
from magma.circuit import Circuit
from magma.clock import Clock
from magma.interface import IO
from magma.t import In, Out


# Useful variables for programming LUTs
LUTS_PER_LOGICBLOCK = 2
LOG_BITS_PER_LUT = 4
BITS_PER_LUT = 1 << LOG_BITS_PER_LUT

ZERO = 0
ONE = (1 << BITS_PER_LUT) - 1

A0 = ht.BitVector[16](0xAAAA)
A1 = ht.BitVector[16](0xCCCC)
A2 = ht.BitVector[16](0xF0F0)
A3 = ht.BitVector[16](0xFF00)

I0 = A0
I1 = A1
I2 = A2
I3 = A3

ALL = A0 & A1 & A2 & A3
ANY = A0 | A1 | A2 | A3
PARITY = A0 ^ A1 ^ A2 ^ A3


class SB_LUT4(Circuit):
    io = IO(
        I0=In(Bit),
        I1=In(Bit),
        I2=In(Bit),
        I3=In(Bit),
        O=Out(Bit)
    )
    param_types = {"LUT_INIT": ht.BitVector[16]}


class SB_CARRY(Circuit):
    """Implements (I0&I1)|(I1&I2)|(I2&I0)"""
    io = IO(
        I0=In(Bit),  # must be the same as SB_LUT4 I1 to pack
        I1=In(Bit),  # must be the same as SB_LUT4 I2 to pack
        CI=In(Bit),  # must be from previous SB_LUT4 to pack
        CO=Out(Bit)
    )


class SB_DFF(Circuit):
    """D Flip-Flop"""
    io = IO(
        C=In(Clock),
        D=In(Bit),
        Q=Out(Bit)
    )

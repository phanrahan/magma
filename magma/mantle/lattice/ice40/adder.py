from magma.bit import Bit
from magma.circuit import Circuit
from magma.interface import IO
from magma.mantle.lattice.ice40.plb import SB_CARRY, A0, A1, A2
from magma.mantle.lattice.ice40.lut import LUT2, LUT3
from magma.t import In, Out


def half_adder(I0, I1):
    """Returns (sum, carry)"""
    return LUT2(A0 ^ A1)()(I0, I1), SB_CARRY()(I0, I1, 0)


class HalfAdder(Circuit):
    io = IO(
        I0=In(Bit),
        I1=In(Bit),
        O=Out(Bit),
        COUT=Out(Bit),
    )
    sum, carry = half_adder(io.I0, io.I1)
    io.O @= sum
    io.COUT @= carry


def full_adder(I0, I1, CIN):
    """Returns (sum, carry)"""
    return LUT3(A0 ^ A1 ^ A2)()(I0, I1, CIN), SB_CARRY()(I0, I1, CIN)


class FullAdder(Circuit):
    io = IO(
        I0=In(Bit),
        I1=In(Bit),
        CIN=In(Bit),
        O=Out(Bit),
        COUT=Out(Bit),
    )
    sum, carry = full_adder(io.I0, io.I1, io.CIN)
    io.O @= sum
    io.COUT @= carry

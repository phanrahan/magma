import operator

import magma as m
from magma.mantle.lattice.ice40.adder import HalfAdder, FullAdder
from magma.testing.utils import check_gold


def test_ice40_half_adder():
    class Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            O=m.Out(m.Bit),
            COUT=m.Out(m.Bit),
        )
        O, COUT = HalfAdder()(io.I0, io.I1)
        io.O @= O
        io.COUT @= COUT

    m.compile("build/test_ice40_half_adder", Top, output="mlir-verilog")
    assert check_gold(__file__, "test_ice40_half_adder.v")


def test_ice40_fulladder():
    class Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            CIN=m.In(m.Bit),
            O=m.Out(m.Bit),
            COUT=m.Out(m.Bit),
        )
        O, COUT = FullAdder()(io.I0, io.I1, io.CIN)
        io.O @= O
        io.COUT @= COUT

    m.compile("build/test_ice40_full_adder", Top, output="mlir-verilog")
    assert check_gold(__file__, "test_ice40_full_adder.v")

import hwtypes as ht

import magma as m
from magma.mantle.lattice.ice40.plb import SB_LUT4, SB_CARRY, SB_DFF
from magma.testing.utils import check_gold


def test_sb_lut4():

    class Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            I2=m.In(m.Bit),
            I3=m.In(m.Bit),
            O=m.Out(m.Bit)
        )
        io.O @= SB_LUT4(LUT_INIT=ht.BitVector[16](0xBEEF))(
            io.I0,
            io.I1,
            io.I2,
            io.I3
        )

    m.compile("build/test_sb_lut4", Top, output="mlir-verilog")
    assert check_gold(__file__, "test_sb_lut4.v")


def test_sb_carry():

    class Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            I2=m.In(m.Bit),
            CI=m.In(m.Bit),
            CO=m.Out(m.Bit)
        )
        io.CO @= SB_CARRY()(io.I0, io.I1, io.CI)

    m.compile("build/test_sb_carry", Top, output="mlir-verilog")
    assert check_gold(__file__, "test_sb_carry.v")


def test_sb_dff():

    class Top(m.Circuit):
        io = m.IO(
            C=m.In(m.Clock),
            D=m.In(m.Bit),
            Q=m.Out(m.Bit),
        )
        io.Q @= SB_DFF()(io.D)

    m.compile("build/test_sb_dff", Top, output="mlir-verilog")
    assert check_gold(__file__, "test_sb_dff.v")

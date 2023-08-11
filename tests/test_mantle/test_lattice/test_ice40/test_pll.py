import magma as m
from magma.mantle.lattice.ice40.pll import SB_PLL
from magma.testing.utils import check_gold


def test_sb_pll():

    class Top(m.Circuit):
        io = m.IO(
            REFERENCECLK=m.In(m.Clock),
            RESETB=m.In(m.Bit),
            BYPASS=m.In(m.Bit),
            PLLOUTCORE=m.Out(m.Bit),
            PLLOUTGLOBAL=m.Out(m.Clock)
        )
        pll = SB_PLL(32000000, 16000000)()
        pll.REFERENCECLK @= io.REFERENCECLK
        pll.RESETB @= io.RESETB
        pll.BYPASS @= io.BYPASS
        io.PLLOUTCORE @= pll.PLLOUTCORE
        io.PLLOUTGLOBAL @= pll.PLLOUTGLOBAL

    m.compile("build/test_sb_pll", Top, output="mlir-verilog")
    assert check_gold(__file__, "test_sb_pll.v")

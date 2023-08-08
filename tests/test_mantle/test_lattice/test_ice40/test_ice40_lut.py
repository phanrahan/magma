import operator

import magma as m
from magma.mantle.lattice.ice40.lut import LUT2, LUT3
from magma.mantle.lattice.ice40.plb import A0, A1, A2, SB_LUT4


def test_ice40_lut2():
    lut = LUT2(A0 ^ A1)
    assert all(map(operator.is_, lut.interface.outputs(), (lut.I0, lut.I1)))
    assert all(map(operator.is_, lut.interface.inputs(), (lut.O,)))
    assert len(lut.instances) == 1
    assert isinstance(lut.instances[0], SB_LUT4)
    assert lut.instances[0].kwargs == {"LUT_INIT": A0 ^ A1}


def test_ice40_lut3():
    lut = LUT3(A0 ^ A1 ^ A2)
    assert all(
        map(operator.is_, lut.interface.outputs(), (lut.I0, lut.I1, lut.I2))
    )
    assert all(map(operator.is_, lut.interface.inputs(), (lut.O,)))
    assert len(lut.instances) == 1
    assert isinstance(lut.instances[0], SB_LUT4)
    assert lut.instances[0].kwargs == {"LUT_INIT": A0 ^ A1 ^ A2}

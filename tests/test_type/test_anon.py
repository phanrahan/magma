from magma import *
from magma.testing import check_files_equal


def test_anon_bit():
    b0 = Bit(name='b0')
    assert b0.direction is None

    b1 = Bit()
    assert b1.direction is None

    # b0 is treated as an output connected to b1 (treated as input)
    wire(b0, b1)
    assert b0 is b1._wire.driver.bit
    assert b1 is b0._wire.driving()[0]
    assert b1.value() is b0
    assert b0.driving() == [b1]
    assert b0.value() is b1


def test_anon_bits():
    class Test(Circuit):
        io = IO(I=In(Bits[5]), O=Out(Bits[5]))

        x = Bits[5]()
        y = Bits[5]()
        y @= io.I
        x @= y
        io.O @= x
    compile("build/test_anon_bits", Test, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/test_anon_bits.v",
                             f"gold/test_anon_bits.v")

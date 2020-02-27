import magma as m
from magma.testing import check_files_equal


def test_undriven():
    class A(m.Product):
        B = m.In(m.Bit)
        C = m.In(m.Bit)

    class Circuit(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bits[5]),
            I2=A,
            I3=m.In(m.Array[5, A]),
        )

        io.I0.unused()
        io.I1.unused()
        io.I2.unused()
        io.I3.unused()

    m.compile("build/test_unused", Circuit)
    assert check_files_equal(__file__, f"build/test_unused.v",
                             f"gold/test_unused.v")

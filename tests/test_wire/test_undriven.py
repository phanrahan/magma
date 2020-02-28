import magma as m
from magma.testing import check_files_equal


def test_undriven():
    class A(m.Product):
        B = m.Out(m.Bit)
        C = m.Out(m.Bit)

    class Circuit(m.Circuit):
        io = m.IO(
            O0=m.Out(m.Bit),
            O1=m.Out(m.Bits[5]),
            O2=A,
            O3=m.Out(m.Array[5, A]),
        )

        io.O0.undriven()
        io.O1.undriven()
        io.O2.undriven()
        io.O3.undriven()

    m.compile("build/test_undriven", Circuit)
    assert check_files_equal(__file__, f"build/test_undriven.v",
                             f"gold/test_undriven.v")

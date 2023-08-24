import magma as m
from magma.testing import check_files_equal


def test_magma_add_default_clock():

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= m.register(io.I)

    basename = "test_circuit_add_default_clock"
    m.compile(f"build/{basename}", Foo)
    assert check_files_equal(
        __file__, f"build/{basename}.v", f"gold/{basename}.v")


def test_magma_add_default_clock_not_used():

    class Bar(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= io.I

    basename = "test_circuit_add_default_clock_not_used"
    m.compile(f"build/{basename}", Bar)
    assert check_files_equal(
        __file__, f"build/{basename}.v", f"gold/{basename}.v")

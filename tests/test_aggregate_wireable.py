import pytest
import magma as m


@pytest.mark.parametrize('T', [m.Bits[8], m.Tuple[m.Bit, m.Bits[8]]])
def test_aggregate_wireable_unwire(T):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I
        assert io.O.value() is io.I
        io.O.unwire(io.I)
        assert io.O.value() is None

        io.O @= io.I
        io.O[0]  # Trigger elaboration
        assert io.O.value() is io.I
        io.O.unwire(io.I)
        assert io.O.value() is None


@pytest.mark.skip("Slow test should only be run if needed")
def test_aggregate_wireable_recursion_error():
    class T(m.Product):
        x = m.Array[2, m.Bits[8]]
        y = m.Bit

    class Foo(m.Circuit):
        T = m.Array[1024, m.Bits[8]]
        io = m.IO(I=m.In(T), O=m.Out(T), S=m.In(m.Bit))
        x = io.I
        for i in range(256):
            prev = x
            x = T(name=f"asdf{i}")
            x @= prev
        io.O @= x

    repr(Foo)

    m.compile("build/Foo", Foo, output="mlir-verilog")

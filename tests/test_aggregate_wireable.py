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

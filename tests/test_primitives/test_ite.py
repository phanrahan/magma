import pytest
import magma as m


def test_ite_signed_unsigned():
    class Main(m.Circuit):
        io = m.IO(a=m.In(m.SInt[16]), b=m.In(m.UInt[16]), s=m.In(m.Bit))

        with pytest.raises(TypeError) as e:
            io.s.ite(io.a, io.b)

        assert str(e.value) == (
            "Found incompatible types SInt[16] and UInt[16] in mux inference")

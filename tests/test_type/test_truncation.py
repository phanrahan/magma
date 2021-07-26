import magma as m
import pytest


def test_python_int_truncation_error():
    with pytest.raises(ValueError) as e:
        class Foo(m.Circuit):
            io = m.IO(x=m.In(m.Bits[2]), y=m.Out(m.Bits[2]))
            io.y @= io.x & 4
    assert str(e.value) == ("Cannot construct Array[2, Out(Bit)] with integer "
                            "4 (requires truncation)")


def test_python_int_truncation_error_2():
    with pytest.raises(ValueError) as e:
        class Foo(m.Circuit):
            io = m.IO(x=m.In(m.Bits[2]), y=m.Out(m.Bits[2]))
            io.y @= io.x & m.bits(4, 2)
    assert str(e.value) == "Cannot convert 4 to a Bits of length 2"

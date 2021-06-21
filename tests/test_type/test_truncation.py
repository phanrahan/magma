import magma as m
import pytest


def test_python_int_truncation_error():
    with pytest.raises(ValueError):
        class Foo(m.Circuit):
            io = m.IO(x=m.In(m.Bits[2]), y=m.Out(m.Bits[2]))
            io.y @= io.x & 4

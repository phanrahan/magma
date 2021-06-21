import pytest
import magma as m


def test_compile_empty_top():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

    with pytest.raises(m.MagmaCompileException):
        m.compile("build/Main", Main)

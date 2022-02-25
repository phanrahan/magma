import pytest
import magma as m


def test_undriven():
    class Foo(m.Circuit):
        io = m.IO(x=m.Out(m.Bit), y=m.Out(m.Bit))
        io.x @= 1

    with pytest.raises(m.compile_exception.MagmaCompileException) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == "Found circuit with errors: Foo"

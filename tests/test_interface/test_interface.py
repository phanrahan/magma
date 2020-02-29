import magma as m
from magma.testing.utils import has_error


def test_1():
    I0 = m.DeclareInterface("a", m.In(m.Bit), "b", m.Out(m.Bits[2]))
    assert str(I0) == '"a", In(Bit), "b", Out(Bits[2])'

    i0 = I0()
    assert str(i0) == '"a", In(Bit), "b", Out(Bits[2])'


def test_io_class_basic():
    expected_names = ["y", "x"]
    expected_types = [m.In(m.Bit), m.Out(m.Bits[8])]
    io = m.IO(y=m.In(m.Bit), x=m.Out(m.Bits[8]))
    assert list(io.ports.keys()) == expected_names
    ports = list(io.ports.values())
    assert all(type(ports[i]) is expected_types[i].flip() for i in range(2))
    assert all(io.decl()[i*2+1] is expected_types[i] for i in range(2))
    assert io.decl()[::2] == expected_names
    for port in io.ports.values():
        assert isinstance(port.name, m.DefnRef)


def test_io_class_bind(caplog):
    io = m.IO(y=m.In(m.Bit), x=m.Out(m.Bits[8]))

    class _Foo(m.Circuit):
        pass

    io.bind(_Foo)
    for port in io.ports.values():
        assert isinstance(port.name, m.DefnRef)
        assert port.name.defn is _Foo

    # Check that calling bind() again logs an error.
    io.bind(_Foo)
    assert has_error(caplog, "Can not bind IO multiple times")

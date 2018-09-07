from magma import DeclareFromVerilog
import inspect
import os
import magma as m


def full_path(filename):
    file_path = os.path.dirname(__file__)
    return os.path.join(file_path, filename)


def test_simple():
    path = full_path("simple.v")
    with open(path, 'r') as f:
        s = f.read()
    v = DeclareFromVerilog(s)
    top = v[0]
    assert top.name == "top"
    assert repr(top.IO) == "Interface(a, In(Bit), b, Out(Bit), c, InOut(Bit))"


def test_type_map():
    path = full_path("simple.v")
    with open(path, 'r') as f:
        s = f.read()
    type_map = {"a": m.In(m.Clock)}
    v = DeclareFromVerilog(s, type_map)
    top = v[0]
    assert repr(top.IO) == "Interface(a, In(Clock), b, Out(Bit), c, InOut(Bit))"


def test_type_map_error():
    path = full_path("simple.v")
    with open(path, 'r') as f:
        s = f.read()
    type_map = {"a": m.In(m.Bits(4))}
    v = DeclareFromVerilog(s, type_map)
    assert len(v) == 0


def test_small():
    path = full_path("small.v")
    small = m.DeclareFromVerilogFile(path)[0]
    for name in small.IO():
        assert name in ["in", "out"]

    for name in small.interface:
        assert name in ["in", "out"]

    for item in small.interface.items():
        assert item in [("in", m.In(m.Bit)), ("out", m.Out(m.Bit))]

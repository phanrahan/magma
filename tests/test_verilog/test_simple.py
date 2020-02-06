from magma import DeclareFromVerilog
import inspect
import os
import pytest
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


@pytest.mark.parametrize("target_type", [m.Clock, m.Reset, m.Bit])
def test_type_map_bit(target_type):
    path = full_path("simple.v")
    with open(path, 'r') as f:
        s = f.read()
    type_map = {"a": m.In(target_type)}
    v = DeclareFromVerilog(s, type_map)
    top = v[0]
    expected = (f"Interface(a, In({repr(target_type)}), b, Out(Bit), c, "
                "InOut(Bit))")
    assert repr(top.IO) == expected


@pytest.mark.parametrize("target_type", [m.Bits[8], m.UInt[8], m.SInt[8]])
def test_type_map_bits(target_type):
    path = full_path("rxmod.v")
    with open(path, 'r') as f:
        s = f.read()
    type_map = {"data": m.Out(target_type)}
    v = DeclareFromVerilog(s, type_map)
    top = v[0]
    expected = (f"Interface(RX, In(Bit), CLK, In(Bit), data, "
                f"Out({target_type}), valid, Out(Bit))")
    assert repr(top.IO) == expected


def test_type_map_error():
    path = full_path("simple.v")
    with open(path, 'r') as f:
        s = f.read()
    type_map = {"a": m.In(m.Bits[4])}
    with pytest.raises(NotImplementedError) as pytest_e:
        v = DeclareFromVerilog(s, type_map)
        assert False
    assert pytest_e.type is NotImplementedError
    assert pytest_e.value.args == \
        ("Conversion between In(Bit) and In(Bits[4]) not supported",)


def test_small():
    path = full_path("small.v")
    small = m.DeclareFromVerilogFile(path)[0]
    for name in small.IO():
        assert name in ["in", "out"]

    for name in small.interface:
        assert name in ["in", "out"]

    for item in small.interface.items():
        assert item in [("in", m.In(m.Bit)), ("out", m.Out(m.Bit))]

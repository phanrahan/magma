from magma import DeclareFromVerilog
import inspect
import os
import magma as m

def test_simple():
    file_path = os.path.dirname(__file__)
    file_name = os.path.join(file_path, "simple.v")
    with open(file_name, 'r') as f:
        s = f.read()

    v = DeclareFromVerilog(s)
    top = v[0]
    assert top.name == "top"
    assert repr(top.IO) == "Interface(a, In(Bit), b, Out(Bit), c, InOut(Bit))"

def test_small():
    file_path = os.path.dirname(__file__)
    file_name = os.path.join(file_path, "small.v")
    small = m.DeclareFromVerilogFile(file_name)[0]
    for name in small.IO():
        assert name in ["in", "out"]

    for name in small.interface:
        assert name in ["in", "out"]

    for item in small.interface.items():
        assert item in [("in", m.In(m.Bit)), ("out", m.Out(m.Bit))]

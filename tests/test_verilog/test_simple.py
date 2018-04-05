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
    assert repr(top.IO) == "Interface(a, In(Bit), b, Out(Bit), c, Bit)"

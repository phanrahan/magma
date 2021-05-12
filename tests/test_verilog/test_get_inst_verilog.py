import os
import magma as m


class T(m.Product):
    x = m.Bit
    y = m.Bits[2]


def test_get_inst_verilog():
    dirname = os.path.abspath(os.path.dirname(__file__))
    os.system(f"cd {dirname} && python foo.py")
    # TODO: Need API to load with a symbol table
    # Also, would be nice to derive a wrapper (e.g. reconstruct the tuples)
    Foo = m.define_from_verilog_file(f"{dirname}/build/Foo.v")[0]

    class Main(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= T(*Foo()(io.I.x, io.I.y))

    m.compile("build/Main", Main)

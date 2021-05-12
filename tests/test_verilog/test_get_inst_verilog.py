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
        foo = Foo()
        # TODO: If we can reconstruct the original tuple for foo, we can just
        # pass the packed tuple rather than x, y individually
        io.O @= T(*foo(io.I.x, io.I.y))
        # TODO: Need API to refer to instance nested inside a verilog imported
        # module (resolved using the symbol table)
        # Proposed API is to pass a name for instances, hierarchical reference
        # using a variable number of string arguments
        # Then the instance reference provides attributes for magma's standard
        # type syntax (e.g. dot notation tuples, subscript for arrays)
        ref = foo.get_instance("bar", "baz").O.x[1]
        m.inline_verilog('assert ({A} == 1) else $error("ERROR");', A=ref)

    m.compile("build/Main", Main)

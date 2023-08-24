import os
import magma as m


def test_no_unused():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]))
        io.I.unused()

    m.compile("build/Foo", Foo, verilator_compat=True)
    path = os.path.join(os.path.dirname(__file__), "build", "Foo.v")
    assert not os.system(
        f"verilator --lint-only -Wall -Wno-DECLFILENAME {path}")

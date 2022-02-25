"""
Test the ability to ignore undriven inputs (useful for formal verification
tools that use undriven inputs to mark wires that can take on any value)
"""
import magma as m
from magma.testing import check_files_equal


def test_ignore_unused_undriven_basic():
    class Main(m.Circuit):
        _ignore_undriven_ = True
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        temp = io.I == 1


    m.compile("build/test_ignore_unused_undriven_basic", Main, inline=True,
              drive_undriven=True, terminate_unused=True)
    assert check_files_equal(__file__,
                             "build/test_ignore_unused_undriven_basic.v",
                             "gold/test_ignore_unused_undriven_basic.v")


def test_ignore_unused_undriven_hierarchy():
    class Foo(m.Circuit):
        _ignore_undriven_ = True
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit),
                  O0=m.Out(m.Bit), O1=m.Out(m.Bit))

        io.O1 @= io.I0

    class Main(m.Circuit):
        _ignore_undriven_ = True
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit),
                  O0=m.Out(m.Bit), O1=m.Out(m.Bit))

        foo = Foo()
        foo.I0 @= io.I0
        io.O0 @= foo.O0


    m.compile("build/test_ignore_unused_undriven_hierarchy", Main, inline=True,
              drive_undriven=True, terminate_unused=True)
    assert check_files_equal(__file__,
                             "build/test_ignore_unused_undriven_hierarchy.v",
                             "gold/test_ignore_unused_undriven_hierarchy.v")

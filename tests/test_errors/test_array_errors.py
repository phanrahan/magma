import pytest

import magma as m


def test_array_partial_unwired():
    class Foo(m.Circuit):
        io = m.IO(A=m.Out(m.Bits[2]))
        io.A[0] @= 1

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A
    Foo.A[0]: Connected
    Foo.A[1]: Unconnected\
"""


def test_array_partial_unwired_nested():
    class Foo(m.Circuit):
        io = m.IO(A=m.Out(m.Array[2, m.Bits[2]]))
        io.A[0] @= 1

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A
    Foo.A[0]: Connected
    Foo.A[1]: Unconnected\
"""


def test_array_partial_unwired_nested2():
    class Foo(m.Circuit):
        io = m.IO(A=m.Out(m.Array[2, m.Bits[2]]))
        io.A[0] @= 1
        io.A[1][0] @= 1

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A
    Foo.A[0]: Connected
    Foo.A[1]
        Foo.A[1][0]: Connected
        Foo.A[1][1]: Unconnected\
"""

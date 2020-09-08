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


@pytest.mark.parametrize("_slice", [slice(1, 4), slice(3, 4), slice(-1, -4),
                                    slice(-3, -4)])
def test_invalid_slice(_slice):
    class Foo(m.Circuit):
        io = m.IO(A=m.Out(m.Array[2, m.Bits[2]]))
        with pytest.raises(IndexError) as e:
            io.A[_slice]
        assert str(e.value) == ("array index out of range "
                                f"(type=Array[2, In(Bits[2])], key={_slice})")

import pytest

import magma as m


def test_product_partial_unwired():
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(T))
        io.A.x @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A
    Foo.A.x: Connected
    Foo.A.y: Unconnected\
"""


def test_product_partial_nested_unwired():
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class U(m.Product):
        x = T
        y = T

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(U), B=m.In(T))
        io.A.x @= io.B

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A
    Foo.A.x: Connected
    Foo.A.y: Unconnected\
"""


def test_product_partial_nested_unwired2():
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class U(m.Product):
        x = T
        y = T

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(U), B=m.In(T))
        io.A.x @= io.B
        io.A.y.x @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A
    Foo.A.x: Connected
    Foo.A.y
        Foo.A.y.x: Connected
        Foo.A.y.y: Unconnected\
"""


def test_product_arr():
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(m.Array[2, T]))
        io.A[0].x @= 0
        io.A[1].y @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A
    Foo.A[0]
        Foo.A[0].x: Connected
        Foo.A[0].y: Unconnected
    Foo.A[1]
        Foo.A[1].x: Unconnected
        Foo.A[1].y: Connected\
"""

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


def test_product_width_mismatch(caplog):
    class T(m.Product):
        x = m.Bits[2]
        y = m.Bits[4]

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(T), B=m.Out(T))
        io.A.x @= m.bits(1, 1)
        io.A.y @= m.bits(2, 3)

        io.B.x @= m.bits(1, 2)
        io.B.y @= m.bits(1, 4)

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A
Foo.A: Unconnected\
"""
    assert caplog.messages[0] == """\
Cannot wire bits(1, 1) (Out(Bits[1])) to Foo.A.x (In(Bits[2]))\
"""
    assert caplog.messages[1] == """\
Cannot wire bits(2, 3) (Out(Bits[3])) to Foo.A.y (In(Bits[4]))\
"""


def test_product_width_mismatch2(caplog):
    class T(m.Product):
        x = m.In(m.Bits[4])
        y = m.Out(m.Bits[2])

    class Foo(m.Circuit):
        io = m.IO(A=T, B=T)
        io.A.y @= io.A.x
        io.B.y @= io.A.x[2:]

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == """\
Found unconnected port: Foo.A.y
Foo.A.y: Unconnected\
"""
    assert caplog.messages[0] == """\
Cannot wire Foo.A.x (Out(Bits[4])) to Foo.A.y (In(Bits[2]))\
"""

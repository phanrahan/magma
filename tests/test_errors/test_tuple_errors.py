import pytest

import magma as m
from magma.common import wrap_with_context_manager
from magma.logging import logging_level


@wrap_with_context_manager(logging_level("DEBUG"))
def test_product_partial_unwired(caplog):
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(T), B=m.Out(m.Bit))
        io.A.x @= 0
        io.B @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert caplog.messages[0] == "Foo.A not driven"
    assert caplog.messages[1] == "Foo.A"
    assert caplog.messages[2] == "    Foo.A.x: Connected"
    assert caplog.messages[3] == "    Foo.A.y: Unconnected"


@wrap_with_context_manager(logging_level("DEBUG"))
def test_product_partial_nested_unwired(caplog):
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class U(m.Product):
        x = T
        y = T

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(U), B=m.In(T), C=m.Out(m.Bit))
        io.A.x @= io.B
        io.C @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert caplog.messages[0] == "Foo.A not driven"
    assert caplog.messages[1] == "Foo.A"
    assert caplog.messages[2] == "    Foo.A.x: Connected"
    assert caplog.messages[3] == "    Foo.A.y: Unconnected"


@wrap_with_context_manager(logging_level("DEBUG"))
def test_product_partial_nested_unwired2(caplog):
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class U(m.Product):
        x = T
        y = T

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(U), B=m.In(T), C=m.Out(m.Bit))
        io.A.x @= io.B
        io.A.y.x @= 0
        io.C @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert caplog.messages[0] == "Foo.A not driven"
    assert caplog.messages[1] == "Foo.A"
    assert caplog.messages[2] == "    Foo.A.x: Connected"
    assert caplog.messages[3] == "    Foo.A.y"
    assert caplog.messages[4] == "        Foo.A.y.x: Connected"
    assert caplog.messages[5] == "        Foo.A.y.y: Unconnected"


@wrap_with_context_manager(logging_level("DEBUG"))
def test_product_arr(caplog):
    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(m.Array[2, T]), B=m.Out(m.Bit))
        io.A[0].x @= 0
        io.A[1].y @= 0
        io.B @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert caplog.messages[0] == "Foo.A not driven"
    assert caplog.messages[1] == "Foo.A"
    assert caplog.messages[2] == "    Foo.A[0]"
    assert caplog.messages[3] == "        Foo.A[0].x: Connected"
    assert caplog.messages[4] == "        Foo.A[0].y: Unconnected"
    assert caplog.messages[5] == "    Foo.A[1]"
    assert caplog.messages[6] == "        Foo.A[1].x: Unconnected"
    assert caplog.messages[7] == "        Foo.A[1].y: Connected"


@wrap_with_context_manager(logging_level("DEBUG"))
def test_product_width_mismatch(caplog):
    class T(m.Product):
        x = m.Bits[2]
        y = m.Bits[4]

    class Foo(m.Circuit):
        io = m.IO(A=m.Out(T), B=m.Out(T), C=m.Out(m.Bit))
        io.A.x @= m.bits(1, 1)
        io.A.y @= m.bits(2, 3)

        io.B.x @= m.bits(1, 2)
        io.B.y @= m.bits(1, 4)
        io.C @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)

    assert str(e.value) == "Found circuit with errors: Foo"
    assert caplog.messages[0] == """\
Cannot wire Bits[1](1) (Out(Bits[1])) to Foo.A.x (In(Bits[2]))\
"""
    assert caplog.messages[1] == """\
Cannot wire Bits[3](2) (Out(Bits[3])) to Foo.A.y (In(Bits[4]))\
"""
    assert caplog.messages[2] == "Foo.A not driven"
    assert caplog.messages[3] == "Foo.A: Unconnected"


def test_product_width_mismatch2(caplog):
    class T(m.Product):
        x = m.In(m.Bits[4])
        y = m.Out(m.Bits[2])

    class Foo(m.Circuit):
        io = m.IO(A=T, B=T, C=m.Out(m.Bit))
        io.A.y @= io.A.x
        io.B.y @= io.A.x[2:]
        io.C @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == "Found circuit with errors: Foo"
    assert caplog.messages[0] == """\
Cannot wire Foo.A.x (Out(Bits[4])) to Foo.A.y (In(Bits[2]))\
"""


def test_product_width_mismatch3(caplog):
    class T(m.Product):
        x = m.In(m.Bits[4])
        y = m.Out(m.Bits[2])

    class Foo(m.Circuit):
        io = m.IO(A=T, B=T, C=m.Out(m.Bit))
        io.A.y[0] @= io.A.x[0]  # Partially wired
        io.B.y @= io.A.x[2:]
        io.C @= 0

    with pytest.raises(Exception) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == "Found circuit with errors: Foo"
    expected = """\
Foo.A.y not driven
Foo.A.y
    Foo.A.y[0]: Connected
    Foo.A.y[1]: Unconnected\
"""
    assert "\n".join(caplog.messages) == expected


@wrap_with_context_manager(logging_level("DEBUG"))
def test_unwired_mixed(caplog):
    class T(m.Product):
        x = m.Out(m.Bit)
        y = m.In(m.Bit)

    class Foo(m.Circuit):
        io = m.IO(z=T, I=m.In(m.Bit))

    class Bar(m.Circuit):
        io = m.IO(z=T, I=m.In(m.Bit), O=m.Out(m.Bit))

        foo = Foo()
        foo.I @= io.I
        io.O @= foo.z.x


    assert caplog.messages[0] == "Bar.z.x not driven"
    assert caplog.messages[1] == "Bar.z.x: Unconnected"

    assert caplog.messages[2] == "Foo_inst0.z.y not driven"
    assert caplog.messages[3] == "Foo_inst0.z.y: Unconnected"

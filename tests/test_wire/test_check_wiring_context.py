import pytest
import magma as m
from magma.compile_exception import MagmaCompileException


def test_missing_generator_paren(caplog):
    class Foo(m.Generator2):
        def __init__(self, width):
            self.io = m.IO(x=m.In(m.Bits[width]), y=m.Out(m.Bits[width]))
            self.io.y @= self.io.x

    class Bar(m.Generator2):
        def __init__(self, width):
            self.io = m.IO(a=m.In(m.Bits[width]),
                           z=m.Out(m.Bit))
            self.io.z @= True
            # Missing a paren
            foo = Foo(width)
            # This wires up an invalid value to Foo.y
            m.wire(foo.y, self.io.a)
            # Correct
            foo = Foo(width)()
            m.wire(foo.x, self.io.a)

    with pytest.raises(MagmaCompileException) as e:
        m.compile("build/Bar", Bar(4))
    assert str(e.value) == ("Cannot wire Bar.a to Foo.y because they are not "
                            "from the same definition context")


def test_bad_temp(caplog):
    class Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        z = m.Bits[8]()
        z @= io.x
        io.y @= z
    # Should not raise an error
    m.compile("build/Foo", Foo)

    class Bar(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        io.y @= Foo.z

    with pytest.raises(MagmaCompileException) as e:
        m.compile("build/Bar", Bar)
    assert str(e.value) == ("Cannot wire Foo.x to Bar.y because they are not "
                            "from the same definition context")


def test_bad_temp2(caplog):
    class Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        z = m.Bits[8]()
        z @= io.x
        io.y @= z

    class Bar(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        Foo.z @= io.x
        io.y @= Foo.z

    with pytest.raises(MagmaCompileException) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == ("Cannot wire Bar.x to Foo.y because they are not "
                            "from the same definition context")


def test_bad_portview(caplog):
    class Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        z = m.Bits[8]()
        io.y @= z

    class Bar(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        foo = Foo()
        io.y @= foo(io.x)

    class Baz(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        bar = Bar()
        io.y @= bar(io.x)

    class Biz(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        io.y @= Baz.bar.foo.y

    with pytest.raises(MagmaCompileException) as e:
        m.compile("build/Foo", Biz)
    assert str(e.value) == ("Cannot wire Bar.Foo_inst0.y to Biz.y because they "
                            "are not from the same definition context")


def test_bad_inst(caplog):
    class Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        io.y @= io.x

    class Bar(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        foo = Foo()
        foo.x @= io.x
        io.y @= foo.y

    class Baz(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        bar = Bar()
        Bar.foo.x @= bar.y

    with pytest.raises(MagmaCompileException) as e:
        m.compile("build/Bar", Bar)
    assert str(e.value) == ("Cannot wire Baz.Bar_inst0.y to Bar.Foo_inst0.x "
                            "because they are not from the same definition "
                            "context")


def test_bad_defn(caplog):
    class Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        io.y @= io.x

    class Bar(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]))
        io.y @= Foo.x

    with pytest.raises(MagmaCompileException) as e:
        m.compile("build/Bar", Bar)
    assert str(e.value) == ("Cannot wire Foo.x to Bar.y "
                            "because they are not from the same definition "
                            "context")

    class Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]), y=m.Out(m.Bits[8]), z=m.Out(m.Bits[8]))
        io.z @= io.x
        io.y @= io.x

    class Bar(m.Circuit):
        io = m.IO(x=m.In(m.Bits[8]))
        Foo.y @= io.x

    with pytest.raises(MagmaCompileException) as e:
        m.compile("build/Foo", Foo)
    assert str(e.value) == ("Cannot wire Bar.x to Foo.y "
                            "because they are not from the same definition "
                            "context")

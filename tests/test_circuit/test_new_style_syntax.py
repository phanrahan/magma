import magma as m
from magma.testing.utils import has_warning, has_error


def _check_foo_interface(Foo):
    assert list(Foo.interface.ports.keys()) == ["I", "O"]
    assert isinstance(Foo.interface.ports["I"], m.Bit)
    assert Foo.interface.ports["I"].is_output()
    assert isinstance(Foo.interface.ports["O"], m.Bit)
    assert Foo.interface.ports["O"].is_input()    


def test_new_style_basic():
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(io.I, io.O)

    assert _Foo.name == "_Foo"
    assert m.isdefinition(_Foo)
    _check_foo_interface(_Foo)


def test_new_style_name():
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        name = "new_name"

    assert _Foo.name == "new_name"


def test_new_style_with_instance():
    instances = []

    class _Bar(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(io.I, io.O)

    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        bar = _Bar()
        m.wire(io.I, bar.I)
        m.wire(bar.O, io.O)
        instances.append(bar)

    assert _Foo.instances == instances
    assert _Foo.O.value() is instances[0].O
    assert instances[0].I.value() is _Foo.I


def test_old_style_override(caplog):
    class _Foo(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]
        io = None  # doesn't matter what the value of io is.

    _check_foo_interface(_Foo)
    expected = "'IO' and 'io' should not both be specified, ignoring 'io'"
    assert has_warning(caplog, expected)


def test_new_style_not_isdefinition():
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

    assert not m.isdefinition(_Foo)


def test_new_style_unconnected(caplog):
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bits[2]))

        m.wire(io.I, io.O[0])

    assert m.isdefinition(_Foo)
    assert has_error(caplog, "Output port _Foo.O not driven")


def test_new_style_with_definition_method(caplog):
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        m.wire(io.I, io.O)

        @classmethod
        def definition(io):
            raise Exception()

    assert m.isdefinition(_Foo)
    expected = ("Supplying method 'definition' with new inline definition "
                "syntax is not supported, ignoring 'definition'")
    assert has_warning(caplog, expected)


def test_new_style_wiring_error(caplog):
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.In(m.Bit))

        m.wire(io.I, io.O)

    assert not m.isdefinition(_Foo)
    assert has_error(caplog, "Using `.O` (an output) as an input")


def test_nested_definition():
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        class _Bar(m.Circuit):
            io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

            m.wire(io.I, io.O)

        bar = _Bar()
        m.wire(io.I, bar.I)
        m.wire(bar.O, io.O)

    assert repr(_Foo) == """_Foo = DefineCircuit("_Foo", "I", In(Bit), "O", Out(Bit))
_Bar_inst0 = _Bar()
wire(_Foo.I, _Bar_inst0.I)
wire(_Bar_inst0.O, _Foo.O)
EndCircuit()"""
    assert repr(_Foo._Bar) == """_Bar = DefineCircuit("_Bar", "I", In(Bit), "O", Out(Bit))
wire(_Bar.I, _Bar.O)
EndCircuit()"""

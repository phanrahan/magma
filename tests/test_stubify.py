import pytest

import magma as m
from magma.testing.utils import has_warning


class _MixedTuple(m.Product):
    x = m.In(m.Bit)
    y = m.Out(m.Bit)


def _make_io():
    return m.IO(
        I=m.In(m.Bit),
        I0=m.In(m.Array[8, m.Bits[10]]),
        mixed=_MixedTuple,
        O=m.Out(m.Bit),
        O3=m.Out(m.Array[4, m.Bits[6]]),
    )


def _get_inputs(obj):
    yield obj.O
    yield obj.mixed.y
    yield from obj.O3


def _get_outputs(obj):
    yield obj.I
    yield from obj.I0
    yield obj.mixed.x


def _check_open_not_implemented(cls):
    with pytest.raises(NotImplementedError):
        cls.open()


def test_stubify_ckt():

    class _Foo(m.Circuit):
        io = _make_io()

    m.stubify(_Foo, stubbifier=m.zero_stubbifier)

    assert m.isdefinition(_Foo)
    _check_open_not_implemented(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)


def test_decorator():

    @m.circuit_stub(stubbifier=m.zero_stubbifier)
    class _Foo(m.Circuit):
        io = _make_io()

    assert m.isdefinition(_Foo)
    _check_open_not_implemented(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)


def test_subclass():

    class _Foo(m.CircuitStub):
        io = _make_io()

    assert m.isdefinition(_Foo)
    _check_open_not_implemented(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)


def test_io():

    class _Foo(m.Circuit):
        io = _make_io()
        m.stubify(io, stubbifier=m.zero_stubbifier)

    assert m.isdefinition(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)


def test_instance():

    class _Foo(m.Circuit):
        io = _make_io()
        # NOTE(rsetaluri): This stubbification is not the one we care about. It
        # is just here to facilitate stubbing the instance of this circuit
        # below.
        m.stubify(io)

    class _(m.Circuit):
        io = m.IO()
        inst = _Foo()
        m.stubify(inst.interface, stubbifier=m.zero_stubbifier)
        # NOTE(rsetaluri): We have to use map() here because of quirks with
        # doing list comprehension inside of class bodies.
        drivers = map(lambda p: p.trace(), _get_outputs(inst))
        assert all(map(lambda d: d.const() and int(d) == 0, drivers))


@pytest.mark.parametrize(
    "stubbifier",
    (
        m.zero_stubbifier,
        m.no_override_driven_zero_stubbifier
    )
)
def test_partially_driven(caplog, stubbifier):

    class _Foo(m.Circuit):
        io = m.IO(O=m.Out(m.Bits[2]))
        io.O @= 1
        m.stubify(io, stubbifier=stubbifier)

    expected_warning = (stubbifier is m.zero_stubbifier)

    if expected_warning:
        assert has_warning(caplog)


def test_clocks():

    class _Foo(m.Circuit):
        io = m.IO()
        reg = m.Register(m.Bit)()
        m.stubify(reg.interface)

    assert _Foo.reg.I.driven()
    driver = _Foo.reg.I.trace()
    assert driver.const() and int(driver) == 0
    assert not _Foo.reg.CLK.driven()


def test_nested_clocks():

    class Clk(m.Product):
        clk = m.Clock

    class _Bar(m.Circuit):
        io = m.IO(I=m.In(m.Bit), clk=m.In(Clk))

    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), clk=m.In(Clk))
        bar = _Bar()
        m.stubify(bar.interface)

    assert _Foo.bar.I.driven()
    driver = _Foo.bar.I.trace()
    assert driver.const() and int(driver) == 0
    assert not _Foo.bar.clk.driven()

import pytest

import magma as m
from magma.testing import check_files_equal


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


def _run_test(cls, out_name, gold_name):
    # Check that open doesn't work.
    with pytest.raises(NotImplementedError):
        cls.open()

    assert m.isdefinition(cls)
    m.compile(f"build/{out_name}", cls, output="coreir")
    assert check_files_equal(
        __file__, f"build/{out_name}.json", f"gold/{gold_name}.json")


def test_stubify_ckt():

    class _Foo(m.Circuit):
        io = _make_io()

    m.stubify(_Foo)
    _run_test(_Foo, "test_stubify_stubify_ckt", "test_stubify")


def test_decorator():

    @m.circuit_stub
    class _Foo(m.Circuit):
        io = _make_io()

    _run_test(_Foo, "test_stubify_decorator", "test_stubify")


def test_subclass():

    class _Foo(m.CircuitStub):
        io = _make_io()

    _run_test(_Foo, "test_stubify_subclass", "test_stubify")

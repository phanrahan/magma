import pytest

import magma as m
from magma.testing import check_files_equal


class _MixedTuple(m.Product):
    x = m.In(m.Bit)
    y = m.Out(m.Bit)


def test_circuit_stub_basic():

    @m.circuit_stub
    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit),
                  I0=m.In(m.Array[8, m.Bits[10]]),
                  mixed=_MixedTuple,
                  O=m.Out(m.Bit),
                  O3=m.Out(m.Array[4, m.Bits[6]]))

    # Check that open doesn't work.
    with pytest.raises(NotImplementedError):
        _Foo.open()

    assert m.isdefinition(_Foo)
    out_name = "test_circuit_stub_basic"
    m.compile(f"build/{out_name}", _Foo, output="coreir")
    assert check_files_equal(
        __file__, f"build/{out_name}.json", f"gold/{out_name}.json")


def test_circuit_stub_subclass():

    class _Foo(m.CircuitStub):
        io = m.IO(I=m.In(m.Bit),
                  I0=m.In(m.Array[8, m.Bits[10]]),
                  mixed=_MixedTuple,
                  O=m.Out(m.Bit),
                  O3=m.Out(m.Array[4, m.Bits[6]]))

    # Check that open doesn't work.
    with pytest.raises(NotImplementedError):
        _Foo.open()

    assert m.isdefinition(_Foo)
    out_name = "test_circuit_stub_subclass"
    m.compile(f"build/{out_name}", _Foo, output="coreir")
    assert check_files_equal(
        __file__,
        f"build/{out_name}.json",
        f"gold/test_circuit_stub_basic.json")

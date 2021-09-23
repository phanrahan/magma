import pytest

import magma as m
from magma.testing import check_files_equal


def _check_compile(name, circ, nested=False):
    if nested:
        name += "_nested"
    m.compile(f"build/{name}", circ)
    assert check_files_equal(__file__, f"build/{name}.v", f"gold/{name}.v")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_basic(nested):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

    _check_compile("test_array2_basic", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_index(nested):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat2(io.I[1:], io.I[:1])

    _check_compile("test_array2_getitem_index", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_slice(nested):
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        if nested:
            T = m.Array2[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat2(io.I[2:], io.I[:2])

    _check_compile("test_array2_getitem_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_wire_to_index(nested):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1]
        io.O[1] @= io.I[0]

    _check_compile("test_array2_wire_to_index", Foo, nested)


def test_array2_wire_to_slice():
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[:2] @= io.I[2:]
        io.O[2:] @= io.I[:2]

    m.compile("build/test_array2_wire_to_slice", Foo)
    assert check_files_equal(__file__, "build/test_array2_wire_to_slice.v",
                             "gold/test_array2_wire_to_slice.v")

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
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1]
        io.O[1] @= io.I[0]

    _check_compile("test_array2_wire_to_index", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_wire_to_slice(nested):
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        if nested:
            T = m.Array2[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[:2] @= io.I[2:]
        io.O[2:] @= io.I[:2]

    _check_compile("test_array2_wire_to_slice", Foo, nested)


def test_array2_tuple():
    class Foo(m.Circuit):
        T = m.Array2[4, m.Tuple[m.Bit, m.Bits[2]]]
        io = m.IO(I=m.In(T),
                  O0=m.Out(T),
                  O1=m.Out(T),
                  O2=m.Out(T),
                  O3=m.Out(T))
        io.O0 @= io.I

        io.O1 @= m.concat2(io.I[2:], io.I[:2])

        io.O2[0] @= io.I[1]
        io.O2[1] @= io.I[0]
        io.O2[2] @= io.I[3]
        io.O2[3] @= io.I[2]

        io.O3[:2] @= io.I[2:]
        io.O3[2:] @= io.I[:2]

    _check_compile("test_array2_tuple", Foo)


def test_tuple_array2():
    class Foo(m.Circuit):
        T = m.Tuple[m.Bit, m.Array2[2, m.Bit]]
        io = m.IO(I=m.In(T),
                  O=m.Out(T))
        io.O[0] @= io.I[0]
        io.O[1][1] @= io.I[1][0]
        io.O[1][0] @= io.I[1][1]

    _check_compile("test_tuple_array2", Foo)


def test_array2_incremental_child_wire():
    class Foo(m.Circuit):
        T = m.Array2[4, m.Tuple[m.Bit, m.Bits[2]]]
        io = m.IO(I=m.In(T), O=m.Out(T))
        for i in range(4):
            io.O[i][0] @= io.I[3 - i][0]
            io.O[i][1] @= io.I[i][1]

    _check_compile("test_array2_incremental_child_wire", Foo)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_slice_of_slice(nested):
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        if nested:
            T = m.Array2[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat2(io.I[1:][:2],
                          io.I[:3][1:])

    _check_compile("test_array2_getitem_slice_of_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_index_of_slice(nested):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1:][0]
        io.O[1] @= io.I[:1][0]

    _check_compile("test_array2_getitem_index_of_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_getitem_index_of_slice(nested):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1:][0]
        io.O[1] @= io.I[:1][0]

    _check_compile("test_array2_getitem_index_of_slice", Foo, nested)


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_index(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1]
        io.O[0] @= io.I[0]
        io.O[1] @= io.I[0]

    _check_compile("test_array2_overlapping_index", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[0], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[0]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_index_slice(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0] @= io.I[1]
        io.O[0:2] @= io.I

    _check_compile("test_array2_overlapping_index_slice", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[0], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[0]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_slice_index(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        if nested:
            T = m.Array2[2, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0:2] @= io.I
        io.O[0] @= io.I[1]

    _check_compile("test_array2_overlapping_slice_index", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[0], Old Output: Foo.I[0], "
                                          "New Output: Foo.I[1]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_slice_slice(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        if nested:
            T = m.Array2[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[0:3] @= io.I[1:]
        io.O[1:4] @= io.I[:3]

    _check_compile("test_array2_overlapping_slice_slice", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[2], "
                                          "New Output: Foo.I[0]")
    assert (str(caplog.records[1].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[2], Old Output: Foo.I[3], "
                                          "New Output: Foo.I[1]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_slice_slice2(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        if nested:
            T = m.Array2[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O[1:4] @= io.I[:3]
        io.O[0:3] @= io.I[1:]

    _check_compile("test_array2_overlapping_slice_slice2", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[0], "
                                          "New Output: Foo.I[2]")
    assert (str(caplog.records[1].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[2], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[3]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_delayed_slice_index(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        if nested:
            T = m.Array2[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        x = io.O[1:4]
        io.O[0] @= io.I[1]
        io.O[1] @= io.I[2]
        x @= io.I[:3]

    _check_compile("test_array2_overlapping_delayed_slice_index", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[2], "
                                          "New Output: Foo.I[0]")


@pytest.mark.parametrize('nested', [False, True])
def test_array2_overlapping_delayed_slice_slice(nested, caplog):
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        if nested:
            T = m.Array2[4, T]
        io = m.IO(I=m.In(T), O=m.Out(T))
        x = io.O[1:4]
        io.O[0:2] @= io.I[0:2]
        x @= io.I[:3]

    _check_compile("test_array2_overlapping_delayed_slice_slice", Foo, nested)
    assert (str(caplog.records[0].msg) == "Wiring multiple outputs to same "
                                          "wire, using last connection. Input: "
                                          "Foo.O[1], Old Output: Foo.I[1], "
                                          "New Output: Foo.I[0]")

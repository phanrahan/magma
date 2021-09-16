import magma as m
from magma.testing import check_files_equal


def test_array2_basic():
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

    m.compile("build/test_array2_basic", Foo)
    assert check_files_equal(__file__, "build/test_array2_basic.v",
                             "gold/test_array2_basic.v")


def test_array2_getitem_index():
    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat2(io.I[1], io.I[0])

    m.compile("build/test_array2_getitem_index", Foo)
    assert check_files_equal(__file__, "build/test_array2_getitem_index.v",
                             "gold/test_array2_getitem_index.v")


def test_array2_getitem_slice():
    class Foo(m.Circuit):
        T = m.Array2[4, m.Bit]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= m.concat2(io.I[2:], io.I[:2])

    m.compile("build/test_array2_getitem_slice", Foo)
    assert check_files_equal(__file__, "build/test_array2_getitem_slice.v",
                             "gold/test_array2_getitem_slice.v")

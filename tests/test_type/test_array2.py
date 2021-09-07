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

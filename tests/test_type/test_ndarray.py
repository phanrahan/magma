import magma as m
from magma.testing import check_files_equal


def test_ndarray_basic():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Array[(3, 5), m.Bit]),
                  O=m.Out(m.Array[(5, 3), m.Bit]))
        for i in range(3):
            for j in range(5):
                io.O[j, i] @= io.I[i, j]
    m.compile("build/test_ndarray_basic", Main)
    assert check_files_equal(__file__, f"build/test_ndarray_basic.v",
                             f"gold/test_ndarray_basic.v")

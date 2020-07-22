import magma as m
from magma.testing import check_files_equal


def test_ndarray_basic():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.NDArray[3, 5]), O=m.Out(m.NDArray[5, 3]))
        for i in range(3):
            for j in range(5):
                io.O[j, i] @= io.I[i, j]
    m.compile("build/test_ndarray_basic", Main)
    assert check_files_equal(__file__, f"build/test_ndarray_basic.v",
                             f"gold/test_ndarray_basic.v")

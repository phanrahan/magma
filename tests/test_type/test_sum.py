import magma as m
from magma.testing.utils import check_gold


def test_sum_basic():
    class T(m.Sum):
        x = m.Bit
        y = m.Bits[2]

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        with m.match(io.I):
            with m.case(io.I, T.x):
                io.O @= ~io.I
            with m.case(io.I, T.y):
                io.O @= io.I ^ 0b11

    m.compile("build/test_sum_basic", Foo, output="mlir-verilog",
              flatten_all_tuples=True)
    assert check_gold(__file__, "test_sum_basic.mlir")

    # TODO: fault support for sum

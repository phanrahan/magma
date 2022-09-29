import magma as m
from magma.testing.utils import check_gold


def test_sum_basic():
    class T(m.Sum):
        x = m.Bit
        y = m.Bits[2]

    class Foo(m.Circuit):
        io = m.IO(
            I0=m.In(T),
            I1=m.In(m.Bits[2]),
            O0=m.Out(T),
            O1=m.Out(m.Bits[2]),
            O2=m.Out(T)
        )
        with m.match(io.I0):
            with m.case(T.x):
                io.O0 @= ~io.I0               # sum  @= sum
                io.O1 @= m.bits(io.I0, 2)     # bits @= sum
                io.O2 @= io.I1[1] ^ io.I1[0]  # sum  @= bits
            with m.case(T.y):
                io.O0 @= io.I0 ^ 0b11  # sum  @= sum
                io.O1 @= io.I0 & 0b01  # bits @= sum
                io.O2 @= io.I1 | 0b10  # sum  @= bits

    m.compile("build/test_sum_basic", Foo, output="mlir",
              flatten_all_tuples=True)
    assert check_gold(__file__, "test_sum_basic.mlir")

    # TODO: fault support for sum

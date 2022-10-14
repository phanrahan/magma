import magma as m


def test_mlir_compiler_finalize_when_order():
    T = m.Tuple[m.Bit, m.Bits[8]]

    class Foo(m.Circuit):
        io = m.IO(I0=m.In(T), I1=m.In(T), S=m.In(m.Bit), O=m.Out(T))
        x = T(name="x")
        with m.when(io.S):
            x @= io.I0
        with m.otherwise():
            x @= io.I1

        io.O @= x

    m.compile("build/Foo", Foo, output="mlir")

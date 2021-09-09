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
    class Concat(m.Circuit):

        io = m.IO(I0=m.In(m.Array2[1, m.Bit]), I1=m.In(m.Array2[1, m.Bit]),
                  O=m.Out(m.Array2[2, m.Bit]))

        coreir_genargs = {"width0": 1, "width1": 1}
        coreir_name = "concat"
        coreir_lib = "coreir"
        renamed_ports = m.circuit.coreir_port_mapping

    class Foo(m.Circuit):
        T = m.Array2[2, m.Bit]
        io = m.IO(I=m.In(T), O=m.Out(T))
        # io.O[1] @= io.I[0]
        # io.O[0] @= io.I[1]
        io.O @= Concat()(io.I[1], io.I[0])

    m.compile("build/test_array2_basic", Foo)
    assert check_files_equal(__file__, "build/test_array2_basic.v",
                             "gold/test_array2_basic.v")

import magma as m
from magma.testing import check_files_equal


def test_basic():

    class _Foo(m.Circuit):
        T = m.Array[10, m.Array[12, m.Bits[32]]]
        io = m.IO(I=m.In(T), O=m.Out(T.T.T))
        io.O @= io.I[4][7]

    basename = "test_packed_array_basic"
    opts = {
        "output": "coreir-verilog",
        "use_packed_arrays": True,
    }
    m.compile(f"build/{basename}", _Foo, **opts)
    assert check_files_equal(
        __file__, f"build/{basename}.v", f"gold/{basename}.v")

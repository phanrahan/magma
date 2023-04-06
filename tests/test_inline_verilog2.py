import magma as m
import magma.testing


def test_simple():

    class _Top(m.Circuit):
        name = "inline_verilog2_simple"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), arr=m.In(m.Bits[2]))
        io += m.ClockIO()
        io.O <= m.register(io.I)
        m.inline_verilog2(
            "assert property (@(posedge CLK) {I} |-> ##1 {O});\n",
            O=io.O,
            I=io.I,
        )
        m.inline_verilog2(
            "assert property (@(posedge CLK) {io.arr[0]} |-> ##1 {io.arr[1]});\n",
        )

    m.compile(f"build/test_inline_verilog2_simple", _Top, output="mlir-verilog")
    assert m.testing.check_files_equal(
        __file__,
        f"build/test_inline_verilog2_simple.mlir",
        f"gold/test_inline_verilog2_simple.mlir",
    )

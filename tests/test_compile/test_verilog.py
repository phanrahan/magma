import magma as m
import magma.testing


def test_verilog_body():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        verilog = f"""
always @(*) begin
    O = I;
    // Note we need to escape the newline here or python treats it as regular
    // newline
    $display("%d\\n", I);
end
"""

    m.compile("build/test_verilog_body", Foo, verilog_prefix="baz_")
    assert m.testing.check_files_equal(
        __file__, f"build/test_verilog_body.v",
        f"gold/test_verilog_body.v")

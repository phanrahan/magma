import magma as m
import magma.testing
import pytest


def test_inline_verilog():
    FF = m.define_from_verilog("""
module FF(input I, output reg O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
""", type_map={"CLK": m.In(m.Clock)})[0]

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), arr=m.In(m.Bits[2]))
        io += m.ClockIO()
        io.O <= FF()(io.I)
        m.inline_verilog("""
assert property (@(posedge CLK) {I} |-> ##1 {O});
""", O=io.O, I=io.I)
        m.inline_verilog("""
assert property (@(posedge CLK) {io.arr[0]} |-> ##1 {io.arr[1]});
""")

    m.compile(f"build/test_inline_simple", Main, output="coreir-verilog",
              sv=True, inline=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_simple.sv",
                                       f"gold/test_inline_simple.sv")


def test_inline_tuple():

    RVDATAIN = m.Array[2, m.Product.from_fields("", dict(data=m.In(m.Bits[5]),
                                                         valid=m.In(m.Bit),
                                                         ready=m.Out(m.Bit)))]

    class InnerInnerDelayUnit(m.Circuit):
        name = "InnerInnerDelayUnit"
        io = m.IO(INPUT=RVDATAIN, OUTPUT=m.Flip(RVDATAIN))

    class InnerDelayUnit(m.Circuit):
        io = m.IO(INPUT=RVDATAIN, OUTPUT=m.Flip(RVDATAIN)) + \
            m.ClockIO()

        delay = InnerInnerDelayUnit(name="inner_inner_delay")
        delay.INPUT[0] <= io.INPUT[1]
        delay.INPUT[1] <= io.INPUT[0]
        io.OUTPUT[0] <= delay.OUTPUT[1]
        io.OUTPUT[1] <= delay.OUTPUT[0]

    class DelayUnit(m.Circuit):
        io = m.IO(INPUT=RVDATAIN, OUTPUT=m.Flip(RVDATAIN)) + \
            m.ClockIO()

        delay = InnerDelayUnit(name="inner_delay")
        delay.INPUT[0] <= io.INPUT[1]
        delay.INPUT[1] <= io.INPUT[0]
        io.OUTPUT[0] <= delay.OUTPUT[1]
        io.OUTPUT[1] <= delay.OUTPUT[0]

    class Main(m.Circuit):
        io = m.IO(I=RVDATAIN, O=m.Flip(RVDATAIN)) + \
            m.ClockIO()

        delay = DelayUnit()
        delay.INPUT[0] <= io.I[1]
        delay.INPUT[1] <= io.I[0]
        io.O[1] <= delay.OUTPUT[0]
        io.O[0] <= delay.OUTPUT[1]

        m.inline_verilog("""\
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=io.I[0].valid, ready_out=io.O[1].ready)

        # Test inst ref
        m.inline_verilog("""\
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=delay.INPUT[1].valid, ready_out=delay.OUTPUT[0].ready)

        # Test recursive ref
        m.inline_verilog("""\
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=delay.inner_delay.INPUT[0].valid,
                               ready_out=delay.inner_delay.OUTPUT[1].ready)

        # Test double recursive ref
        m.inline_verilog("""\
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=delay.inner_delay.inner_inner_delay.INPUT[0].valid,
                               ready_out=delay.inner_delay.inner_inner_delay.OUTPUT[1].ready)

    m.compile(f"build/test_inline_tuple", Main, output="coreir-verilog",
              sv=True, inline=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_tuple.sv",
                                       f"gold/test_inline_tuple.sv")

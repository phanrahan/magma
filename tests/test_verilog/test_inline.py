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
""", O=io.O, I=io.I, inline_wire_prefix="_foo_prefix_")
        m.inline_verilog("""
assert property (@(posedge CLK) {io.arr[0]} |-> ##1 {io.arr[1]});
""")

    m.compile(f"build/test_inline_simple", Main, output="coreir-verilog",
              sv=True, inline=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_simple.sv",
                                       f"gold/test_inline_simple.sv")


def test_inline_tuple():

    RVDATAIN = m.Array[2, m.AnonProduct[dict(data=m.In(m.Bits[5]),
                                             valid=m.In(m.Bit),
                                             ready=m.Out(m.Bit))]]

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
assert property (@(posedge CLK) {valid_out} |-> ##3 {ready_out});\
""", valid_out=io.I[0].valid, ready_out=io.O[1].ready)

        # Test inst ref
        m.inline_verilog("""\
assert property (@(posedge CLK) {valid_out} |-> ##3 {ready_out});\
""", valid_out=delay.OUTPUT[1].valid, ready_out=delay.INPUT[0].ready)

        # Test recursive ref
        m.inline_verilog("""\
assert property (@(posedge CLK) {valid_out} |-> ##3 {ready_out});\
""", valid_out=delay.inner_delay.OUTPUT[0].valid,
                               ready_out=delay.inner_delay.INPUT[1].ready)

        # Test double recursive ref
        m.inline_verilog("""\
assert property (@(posedge CLK) {valid_out} |-> ##3 {ready_out});\
""", valid_out=delay.inner_delay.inner_inner_delay.OUTPUT[0].valid,
                               ready_out=delay.inner_delay.inner_inner_delay.INPUT[1].ready)

    m.compile(f"build/test_inline_tuple", Main, output="coreir-verilog",
              sv=True, inline=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_tuple.sv",
                                       f"gold/test_inline_tuple.sv")


def test_inline_loop_var():
    class Main(m.Circuit):
        _ignore_undriven_ = True
        io = m.IO(O=m.Out(m.Array[5, m.Bits[5]]))
        for i in range(5):
            m.inline_verilog("""
assign O[{i}] = {i};
            """)

    m.compile(f"build/test_inline_loop_var", Main, drive_undriven=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_loop_var.v",
                                       f"gold/test_inline_loop_var.v")


def test_clock_inline_verilog():
    class ClockT(m.Product):
        clk = m.Out(m.Clock)
        resetn = m.Out(m.AsyncResetN)

    class Bar(m.Circuit):
        io = m.IO(clks=ClockT)

    class Foo(m.Circuit):
        io = m.IO(clks=m.Flip(ClockT))

        bar = Bar()
        # Since clk is coming from another instance, it is an output Without
        # changing the type to undirected for the temporary signal, we'll get a
        # coreir error:
        #   ERROR: WireOut(Clock) 7 is not a valid coreIR name!. Needs to be =
        #   ^[a-zA-Z_\-\$][a-zA-Z0-9_\-\$]*
        clk = bar.clks.clk

        resetn = m.AsyncResetN()
        resetn @= bar.clks.resetn

        outputVector = m.Bits[8]()
        outputVector @= 0xDE

        outputValid = m.Bit()
        outputValid @= 1

        m.inline_verilog("""
`ASSERT(ERR_output_vector_onehot_when_valid,
        {outputValid} |-> $onehot({outputVector}, {clk}, {resetn})
""")

    # Should not throw a coreir error
    m.compile("build/Foo", Foo, inline=True)


def test_inline_verilog_unique():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit))
        m.inline_verilog('always @(*) $display("%d\\n", {io.I});')

    Bar = Foo

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit))
        m.inline_verilog('always @(*) $display("%x\\n", {io.I});')

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit))
        Bar()(io.I)
        Foo()(io.I)

    m.compile("build/test_inline_verilog_unique", Top)
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_verilog_unique.v",
                                       f"gold/test_inline_verilog_unique.v")

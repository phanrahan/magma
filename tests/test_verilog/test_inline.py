import magma as m
import magma.testing
import pytest


def test_inline_verilog():
    FF = m.DefineFromVerilog("""
module FF(input I, output O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
""", type_map={"CLK": m.In(m.Clock)})[0]

    class Main(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)] + m.ClockInterface()
        @classmethod
        def definition(cls):
            cls.O <= FF()(cls.I)
            cls.inline_verilog("""
assert property {{ @(posedge CLK) {I} |-> ##1 {O} }};
""", O=cls.O, I=cls.I)

    m.compile(f"build/test_inline_simple", Main, output="coreir")
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_simple.json",
                                       f"gold/test_inline_simple.json")


def test_inline_tuple():

    RVDATAIN = m.Array[2, m.Tuple(data=m.In(m.Bits[5]), valid=m.In(m.Bit),
                                  ready=m.Out(m.Bit))]

    InnerInnerDelayUnit = m.DeclareCircuit("InnerInnerDelayUnit",
                                      "INPUT", RVDATAIN,
                                      "OUTPUT", m.Flip(RVDATAIN))

    class InnerDelayUnit(m.Circuit):
        IO = ["INPUT", RVDATAIN, "OUTPUT", m.Flip(RVDATAIN)] + \
            m.ClockInterface()

        @classmethod
        def definition(cls):
            delay = InnerInnerDelayUnit(name="inner_inner_delay")
            delay.INPUT[0] <= cls.INPUT[1]
            delay.INPUT[1] <= cls.INPUT[0]
            cls.OUTPUT[0] <= delay.OUTPUT[1]
            cls.OUTPUT[1] <= delay.OUTPUT[0]

    class DelayUnit(m.Circuit):
        IO = ["INPUT", RVDATAIN, "OUTPUT", m.Flip(RVDATAIN)] + \
            m.ClockInterface()

        @classmethod
        def definition(cls):
            delay = InnerDelayUnit(name="inner_delay")
            delay.INPUT[0] <= cls.INPUT[1]
            delay.INPUT[1] <= cls.INPUT[0]
            cls.OUTPUT[0] <= delay.OUTPUT[1]
            cls.OUTPUT[1] <= delay.OUTPUT[0]

    class Main(m.Circuit):
        IO = ["I", RVDATAIN, "O", m.Flip(RVDATAIN)] + m.ClockInterface()
        @classmethod
        def definition(cls):
            delay = DelayUnit()
            delay.INPUT[0] <= cls.I[1]
            delay.INPUT[1] <= cls.I[0]
            cls.O[1] <= delay.OUTPUT[0]
            cls.O[0] <= delay.OUTPUT[1]

            cls.inline_verilog("""\
assert property {{ @(posedge CLK) {valid_in} |-> ##3 {ready_out} }};\
""", valid_in=cls.I[0].valid, ready_out=cls.O[1].ready)

            # Test inst ref
            cls.inline_verilog("""\
assert property {{ @(posedge CLK) {valid_in} |-> ##3 {ready_out} }};\
""", valid_in=delay.INPUT[1].valid, ready_out=delay.OUTPUT[0].ready)

            # Test recursive ref
            cls.inline_verilog("""\
assert property {{ @(posedge CLK) {valid_in} |-> ##3 {ready_out} }};\
""", valid_in=delay.inner_delay.INPUT[0].valid,
     ready_out=delay.inner_delay.OUTPUT[1].ready)

            # Test double recursive ref
            cls.inline_verilog("""\
assert property {{ @(posedge CLK) {valid_in} |-> ##3 {ready_out} }};\
""", valid_in=delay.inner_delay.inner_inner_delay.INPUT[0].valid,
     ready_out=delay.inner_delay.inner_inner_delay.OUTPUT[1].ready)

    m.compile(f"build/test_inline_tuple", Main, output="coreir")
    assert m.testing.check_files_equal(__file__,
                                       f"build/test_inline_tuple.json",
                                       f"gold/test_inline_tuple.json")

# Inline Verilog
Magma supports inline verilog as a temporary solution for defining properties and covergroups.

Here's a simple example of a flip flop module imported from verilog
```python
FF = m.DefineFromVerilog("""
module FF(input I, output reg O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
""", type_map={"CLK": m.In(m.Clock)})[0]
```

Now suppose we use this FF in a Circuit
```python
class Main(m.Circuit):
    IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)] + m.ClockInterface()
    @classmethod
    def definition(cls):
        cls.O <= FF()(cls.I)
```

We can add an inline assertion using the `cls.inline_verilog` method
```python
        cls.inline_verilog("""
assert property (@(posedge CLK) {I} |-> ##1 {O});
""", O=cls.O, I=cls.I)
```

The `inline_verilog` interface accepts a templated verilog string (using
Python's format string with keyword arguments syntax) as the first argument,
then a dicitonary of keyword args (`**kwargs`) that map template (format)
variables to magma values.  This allows the user to pass arbitrary magma values
(e.g. Python temporary variables, instance ports, and interface ports).  The
`inline_verilog` method will handle the conversion of the magma value to it's
corresponding verilog name.

Note, since we're using system verilog assertion syntax, we'll need to
pass the option `sv=True` to the `m.compile` command.
```python
m.compile(f"build/test_inline_simple", Main, output="coreir-verilog",
          sv=True, inline=True)
```

This produces the following output
```verilog
module FF(input I, output reg O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
module Main (input CLK, input I, output O);
FF FF_inst0(.CLK(CLK), .I(I), .O(O));

assert property (@(posedge CLK) I |-> ##1 O);

endmodule

```

`inline_verilog` supports passing references to signals using the hierarchical
attribute syntax.  Here's a more complex example that shows various examples of
referring to complex (Tuple) types and child instances.

```python
RVDATAIN = m.Array[2, m.Product.from_fields("", dict(data=m.In(m.Bits[5]),
                                                     valid=m.In(m.Bit),
                                                     ready=m.Out(m.Bit)))]

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
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=cls.I[0].valid, ready_out=cls.O[1].ready)

        # Inst ref
        cls.inline_verilog("""\
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=delay.INPUT[1].valid, ready_out=delay.OUTPUT[0].ready)

        # Child ref
        cls.inline_verilog("""\
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=delay.inner_delay.INPUT[0].valid,
     ready_out=delay.inner_delay.OUTPUT[1].ready)

        # Double child ref
        cls.inline_verilog("""\
assert property (@(posedge CLK) {valid_in} |-> ##3 {ready_out});\
""", valid_in=delay.inner_delay.inner_inner_delay.INPUT[0].valid,
     ready_out=delay.inner_delay.inner_inner_delay.OUTPUT[1].ready)

m.compile(f"build/test_inline_tuple", Main, output="coreir-verilog",
          sv=True)
```

This produces the following verilog
```verilog
// Module `InnerInnerDelayUnit` defined externally
module InnerDelayUnit (
    input CLK,
    input [4:0] INPUT_0_data,
    output INPUT_0_ready,
    input INPUT_0_valid,
    input [4:0] INPUT_1_data,
    output INPUT_1_ready,
    input INPUT_1_valid,
    output [4:0] OUTPUT_0_data,
    input OUTPUT_0_ready,
    output OUTPUT_0_valid,
    output [4:0] OUTPUT_1_data,
    input OUTPUT_1_ready,
    output OUTPUT_1_valid
);
InnerInnerDelayUnit inner_inner_delay(
    .INPUT_0_data(INPUT_1_data),
    .INPUT_0_ready(INPUT_1_ready),
    .INPUT_0_valid(INPUT_1_valid),
    .INPUT_1_data(INPUT_0_data),
    .INPUT_1_ready(INPUT_0_ready),
    .INPUT_1_valid(INPUT_0_valid),
    .OUTPUT_0_data(OUTPUT_1_data),
    .OUTPUT_0_ready(OUTPUT_1_ready),
    .OUTPUT_0_valid(OUTPUT_1_valid),
    .OUTPUT_1_data(OUTPUT_0_data),
    .OUTPUT_1_ready(OUTPUT_0_ready),
    .OUTPUT_1_valid(OUTPUT_0_valid)
);
endmodule

module DelayUnit (
    input CLK,
    input [4:0] INPUT_0_data,
    output INPUT_0_ready,
    input INPUT_0_valid,
    input [4:0] INPUT_1_data,
    output INPUT_1_ready,
    input INPUT_1_valid,
    output [4:0] OUTPUT_0_data,
    input OUTPUT_0_ready,
    output OUTPUT_0_valid,
    output [4:0] OUTPUT_1_data,
    input OUTPUT_1_ready,
    output OUTPUT_1_valid
);
InnerDelayUnit inner_delay(
    .CLK(CLK),
    .INPUT_0_data(INPUT_1_data),
    .INPUT_0_ready(INPUT_1_ready),
    .INPUT_0_valid(INPUT_1_valid),
    .INPUT_1_data(INPUT_0_data),
    .INPUT_1_ready(INPUT_0_ready),
    .INPUT_1_valid(INPUT_0_valid),
    .OUTPUT_0_data(OUTPUT_1_data),
    .OUTPUT_0_ready(OUTPUT_1_ready),
    .OUTPUT_0_valid(OUTPUT_1_valid),
    .OUTPUT_1_data(OUTPUT_0_data),
    .OUTPUT_1_ready(OUTPUT_0_ready),
    .OUTPUT_1_valid(OUTPUT_0_valid)
);
endmodule

module Main (
    input CLK,
    input [4:0] I_0_data,
    output I_0_ready,
    input I_0_valid,
    input [4:0] I_1_data,
    output I_1_ready,
    input I_1_valid,
    output [4:0] O_0_data,
    input O_0_ready,
    output O_0_valid,
    output [4:0] O_1_data,
    input O_1_ready,
    output O_1_valid
);
DelayUnit DelayUnit_inst0(
    .CLK(CLK),
    .INPUT_0_data(I_1_data),
    .INPUT_0_ready(I_1_ready),
    .INPUT_0_valid(I_1_valid),
    .INPUT_1_data(I_0_data),
    .INPUT_1_ready(I_0_ready),
    .INPUT_1_valid(I_0_valid),
    .OUTPUT_0_data(O_1_data),
    .OUTPUT_0_ready(O_1_ready),
    .OUTPUT_0_valid(O_1_valid),
    .OUTPUT_1_data(O_0_data),
    .OUTPUT_1_ready(O_0_ready),
    .OUTPUT_1_valid(O_0_valid)
);
assert property (@(posedge CLK) I_0_valid |-> ##3 O_1_ready);

assert property (@(posedge CLK) DelayUnit_inst0.INPUT_1_valid |-> ##3 DelayUnit_inst0.OUTPUT_0_ready);

assert property (@(posedge CLK) DelayUnit_inst0.inner_delay.INPUT_0_valid |-> ##3 DelayUnit_inst0.inner_delay.OUTPUT_1_ready);

assert property (@(posedge CLK) DelayUnit_inst0.inner_delay.inner_inner_delay.INPUT_0_valid |-> ##3 DelayUnit_inst0.inner_delay.inner_inner_delay.OUTPUT_1_ready);
endmodule


```

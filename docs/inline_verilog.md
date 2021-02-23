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
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()
    io.O <= FF()(io.I)
```

We can add an inline assertion using the `m.inline_verilog` function
```python
    m.inline_verilog("""
assert property (@(posedge CLK) {I} |-> ##1 {O});
""", O=io.O, I=io.I)
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
m.compile(f"build/test_inline_simple", Main, output="coreir-verilog", sv=True,
          inline=True)
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
InnerInnerDelayUnit inner_inner_delay (
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
InnerDelayUnit inner_delay (
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
DelayUnit DelayUnit_inst0 (
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

You can also use a syntax similar to Python's
[f-string](https://www.python.org/dev/peps/pep-0498/) syntax without having to
pass keyword args.

Here's an example:
```python
class RTLMonitor(m.Circuit):
    io = m.IO(**m.make_monitor_ports(circuit),
              mon_temp1=m.In(m.Bit),
              mon_temp2=m.In(m.Bit),
              intermediate_tuple=m.In(m.Tuple[m.Bit, m.Bit]))

    # NOTE: Needs to have a name
    arr_2d = m.Array[2, m.Bits[width]](name="arr_2d")
    for i in range(2):
        arr_2d[i] @= getattr(io, f"in{i + 1}")
    m.inline_verilog("""
logic temp1, temp2;
logic [{width-1}:0] temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & {io.intermediate_tuple[0]};
assign temp3 = in1 ^ in2;
assert property (@(posedge CLK) {io.handshake.valid} -> out === temp1 && temp2);
logic [{width-1}:0] temp4 [1:0];
assign temp4 = {arr_2d};
                           """)
```

Notice that the Python variables `arr_2d` and `io.handshake.valid` are passed
directly to the format string inside curly braces `{...}`.  These expressions
will be interpolated using the same logic as if they were passed as format
keyword arguments to inline_verilog (so values will be converted to their
verilog name).  You can also do basic Python expressions such as `{width - 1}`
which will be executed in Python before being interpolated into the string.

# Bind

To use the `bind` feature, define a subclass of `m.MonitorGenerator` which is
bound to a subclass of `m.Generator` (design generator).  The subclass defines
a staticmethod `generate_bind(circuit, *args, **kwargs)` where `args` and
`kwargs` are the same as the corresponding `m.Generator`'s `generate` method
(reference to the same parameters).  This staticmethod should generate a
monitor circuit and call `circuit.bind(monitor, *args)`.  Extra arguments to
the `bind` method can be used to pass circuit intermediate values.

Here is a full example:

We begin with an `m.Generator` definition for some RTL.
```python
# rtl.py
import magma as m


class RTL(m.Generator):
    @staticmethod
    def generate(width):
        orr, andr, logical_and = m.define_from_verilog(f"""
            module orr_{width} (input [{width - 1}:0] I, output O);
            assign O = |(I);
            endmodule

            module andr_{width} (input [{width - 1}:0] I, output O);
            assign O = &(I);
            endmodule

            module logical_and (input I0, input I1, output O);
            assign O = I0 && I1;
            endmodule
        """)

        class HandShake(m.Product):
            ready = m.In(m.Bit)
            valid = m.Out(m.Bit)

        class RTL(m.Circuit):
            io = m.IO(CLK=m.In(m.Clock),
                      in1=m.In(m.Bits[width]),
                      in2=m.In(m.Bits[width]),
                      out=m.Out(m.Bit),
                      handshake=HandShake,
                      handshake_arr=m.Array[3, HandShake])

            temp1 = orr()(io.in1)
            temp2 = andr()(io.in1)
            intermediate_tuple = m.tuple_([temp1, temp2])
            io.out @= logical_and()(intermediate_tuple[0],
                                    intermediate_tuple[1])
            m.wire(io.handshake.valid, io.handshake.ready)
            for i in range(3):
                m.wire(io.handshake_arr[i].valid,
                       io.handshake_arr[2 - i].ready)
        return RTL
```

We define a corresponding `m.MonitorGenerator`

```python
# rtl_monitor.py
import magma as m
from rtl import RTL


class RTLMonitor(m.MonitorGenerator):
    @staticmethod
    def generate_bind(circuit, width):
        # circuit is a reference to the generated module (to retrieve internal
        # signals and bind to the module)
        class RTLMonitor(m.Circuit):
            io = m.IO(**m.make_monitor_ports(circuit),
                      mon_temp1=m.In(m.Bit),
                      mon_temp2=m.In(m.Bit),
                      intermediate_tuple=m.In(m.Tuple[m.Bit, m.Bit]))

            # NOTE: Needs to have a name
            arr_2d = m.Array[2, m.Bits[width]](name="arr_2d")
            for i in range(2):
                arr_2d[i] @= getattr(io, f"in{i + 1}")
            m.inline_verilog("""
logic temp1, temp2;
logic [{width-1}:0] temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & {io.intermediate_tuple[0]};
assign temp3 = in1 ^ in2;
assert property (@(posedge CLK) {valid} -> out === temp1 && temp2);
logic [{width-1}:0] temp4 [1:0];
assign temp4 = {arr_2d};
                                   """,
                                   valid=io.handshake.valid)

        circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2,
                     circuit.intermediate_tuple)


RTL.bind(RTLMonitor)
```

To bring it all together in another file, we can import `rtl` and `rtl_monitor`
```python
from rtl import RTL
import rtl_monitor
import magma as m

RTL4 = RTL.generate(4)

m.compile("build/bind_test", RTL4, inline=True)
```

If you don't want to enable the bind, simply do not import `rtl_monitor`

The `bind` statement also supports an optional `compile_guard=` keyword
argument that allows the user to wrap the generated bind statement inside a
verilog `ifdef`.  Here's an example:

```python
circuit.bind(RTLMonitor, circuit.temp1, circuit.temp2,
             circuit.intermediate_tuple, compile_guard="BIND_ON")
# generates
# `ifdef BIND_ON
# bind ...
# endif
```

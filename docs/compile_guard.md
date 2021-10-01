# Compile Guard
Magma supports the concept of a *compile guard* that behaves like an `ifdef`
statement in a traditional preprocessor.

This is useful for wrapping parts of a circuit in a *guard* that will allow the
user to enable/disable the inclusion of the hardware in a downstream tool.

One example is logic used for an assertion.  This logic might only be wanted
inside verification flows, but not inside synthesis flows.  To do this, we put
the logic inside a `with compile_guard(...):` statement:

```python
class Foo(m.Circuit):
    io = m.IO(I=m.In(m.Valid[m.Bits[4]]), O=m.Out(m.Bits[4])) + m.ClockIO()
    io.O @= m.Register(m.Bits[4])()(io.I.data)

    with m.compile_guard("ASSERT_ON"):
        # Counter logic only for assertion
        count = m.Register(m.UInt[2], has_enable=True)()
        count.I @= count.O + 1
        count.CE @= io.I.valid

        f.assert_immediate((count.O != 3) | (io.O.value() == 3))
```

This generates the following code (some modules omitted):
```verilog
...

module CompileGuardCircuit_0 (
    input port_0,
    input CLK,
    input [3:0] port_1
);
wire [1:0] Register_inst0_O;
wire _magma_inline_wire0;
wire [1:0] magma_Bits_2_add_inst0_out;
Register_unq1 Register_inst0 (
    .I(magma_Bits_2_add_inst0_out),
    .O(Register_inst0_O),
    .CE(port_0),
    .CLK(CLK)
);
assign _magma_inline_wire0 = (~ (Register_inst0_O == 2'h3)) | (port_1 == 4'h3);
assign magma_Bits_2_add_inst0_out = 2'(Register_inst0_O + 2'h1);
initial assert (_magma_inline_wire0);
endmodule

module Foo (
    input CLK,
    input [3:0] I_data,
    input I_valid,
    output [3:0] O
);
`ifdef ASSERT_ON
CompileGuardCircuit_0 CompileGuardCircuit_0 (
    .port_0(I_valid),
    .CLK(CLK),
    .port_1(O)
);
`endif
Register Register_inst0 (
    .I(I_data),
    .O(O),
    .CLK(CLK)
);
endmodule
```

Notice that the counter logic has been moved inside the module
`CompileGuardCircuit_0` and the instantiation of that module is wrapped inside
a verilog `ifdef`.  Now the user can enable/disable the inclusion of the logic
by using the `ASSERT_ON` define.

Note that logic inside a compile guard cannot be used outside of a compile
guard (otherwise a signal may not have a driver when the guard is disabled).

To generate an `ifndef` instead of `ifdef`, pass the argument
`type="undefined"` to `m.compile_guard` (the default is `type="defined"`).

## compile_guard_select
To conditionally drive a value based on a compile guard, use the
`m.compile_guard_select` function which takes keyword arguments mapping
a compile guard name to a driver.  Use the special keyword argument `default`
to set the default driver.  Here's a simple example:
```python
class Top(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()

    x = m.Register(m.Bit)()(io.I ^ 1)
    y = m.Register(m.Bit)()(io.I)

    io.O @= m.compile_guard_select(
        COND1=x, COND2=y, default=io.I
    )
```

**NOTE:** `compile_guard_select` currently requires that all arguments have the
same type, please convert them first if that's not the case.

**NOTE:** priority for the selected (non-default) driver is defined by the
order of the arguments.  The above example will generate verilog equivalent to
```verilog
`ifdef COND1
    assign O = x;
`elsif COND2
    assign O = y;
`else
    assign O = I;
`endif
```

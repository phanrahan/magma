# m.display

Magma supports using verilog display with the coreir-verilog backend using the
`m.display` function.  This function accepts a standard display format string
as the first argument and a variable number of arguments corresponding to magma
values.  These magma values will be interpolated into the generated display
statement to display their runtime values.

`m.display` returns an object that supports method-chaining for specifying
event triggers and conditions.  For example, to trigger display only on the
positive edge of a clock, one would write `m.display("<str>"
*args).when(m.posedge(io.CLK))`.  Currently magma provides the `m.posedge` and
`m.negedge` events.  You can also guard the display statement with a condition using
the `if_` method, for example to only display when the clock enable is high,
one would write `m.display("<str>").if_(io.CE)`.

Here is a full example:
```python
class Main(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
    ff = FF()
    io.O @= ff(io.I)
    m.display("ff.O=%d, ff.I=%d", ff.O, ff.I).when(m.posedge(io.CLK))\
                                             .if_(io.CE)
```

This produces the following snippet of verilog for the display statement:
```verilog
always @(posedge CLK) begin
    if (CE) $display("ff.O=%d, ff.I=%d", FF_inst0.O, FF_inst0.I);
end
```

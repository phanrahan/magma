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

This generates the following code:
```verilog
module coreir_reg #(
    parameter width = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module corebit_term (
    input in
);

endmodule

module Register (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Mux2xUInt2 (
    input [1:0] I0,
    input [1:0] I1,
    input S,
    output [1:0] O
);
reg [1:0] coreir_commonlib_mux2x2_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x2_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x2_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x2_inst0_out;
endmodule

module Register_unq1 (
    input [1:0] I,
    output [1:0] O,
    input CE,
    input CLK
);
wire [1:0] enable_mux_O;
Mux2xUInt2 enable_mux (
    .I0(O),
    .I1(I),
    .S(CE),
    .O(enable_mux_O)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_P_inst0 (
    .clk(CLK),
    .in(enable_mux_O),
    .out(O)
);
endmodule

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

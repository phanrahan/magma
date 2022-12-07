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

module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module Register (
    input I,
    output O,
    input CLK
);
wire [0:0] _reg_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) _reg (
    .clk(CLK),
    .in(I),
    .out(_reg_out)
);
assign O = _reg_out[0];
endmodule

module A (
    input port_0,
    input port_1
);
wire Register_inst0_O;
Register Register_inst0 (
    .I(port_0),
    .O(Register_inst0_O),
    .CLK(port_1)
);
endmodule

module _Top (
    input I,
    input CLK
);
wire x_out;
`ifdef COND
A A (
    .port_0(x_out),
    .port_1(CLK)
);
`endif
corebit_wire x (
    .in(I),
    .out(x_out)
);
endmodule


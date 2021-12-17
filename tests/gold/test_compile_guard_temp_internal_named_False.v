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

module Register (
    input I,
    output O,
    input CLK
);
wire [0:0] reg_P1_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P1_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P1_inst0_out)
);
assign O = reg_P1_inst0_out[0];
endmodule

module DebugModule (
    input port_0,
    input CLK
);
wire reg_O;
wire reg2_O;
Register reg (
    .I(port_0),
    .O(reg_O),
    .CLK(CLK)
);
Register reg2 (
    .I(\reg _O),
    .O(reg2_O),
    .CLK(CLK)
);
endmodule

module Top (
    input I,
    output O,
    input CLK
);
`ifdef DEBUG
DebugModule DebugModule (
    .port_0(I),
    .CLK(CLK)
);
`endif
assign O = I;
endmodule


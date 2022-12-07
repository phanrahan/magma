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

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = I0;
end else begin
    mux_out = I1;
end
end

assign O = mux_out[0];
endmodule

module Main (
    input s,
    output O0,
    output O1,
    input CLK
);
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire reg_O;
Mux2xBit Mux2xBit_inst0 (
    .I0(\reg _O),
    .I1(magma_Bit_not_inst0_out),
    .S(s),
    .O(O0)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(magma_Bit_not_inst1_out),
    .I1(\reg _O),
    .S(s),
    .O(O1)
);
assign magma_Bit_not_inst0_out = ~ \reg _O;
assign magma_Bit_not_inst1_out = ~ \reg _O;
Register reg (
    .I(O0),
    .O(reg_O),
    .CLK(CLK)
);
endmodule


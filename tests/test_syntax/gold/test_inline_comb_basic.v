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

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Main (
    input invert,
    output O0,
    output O1,
    input CLK
);
wire Mux2xBit_inst0_O;
wire Mux2xBit_inst1_O;
wire O1;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire reg_O;
Mux2xBit Mux2xBit_inst0 (
    .I0(O0),
    .I1(magma_Bit_not_inst0_out),
    .S(invert),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(O0),
    .I1(magma_Bit_not_inst1_out),
    .S(invert),
    .O(Mux2xBit_inst1_O)
);
assign O1 = Mux2xBit_inst1_O;
assign magma_Bit_not_inst0_out = ~ O0;
assign magma_Bit_not_inst1_out = ~ O0;
Register reg (
    .I(Mux2xBit_inst0_O),
    .O(reg_O),
    .CLK(CLK)
);
assign O1 = O1;
endmodule


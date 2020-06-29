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

module commonlib_muxn__N2__width16 (
    input [15:0] in_data_0,
    input [15:0] in_data_1,
    input [0:0] in_sel,
    output [15:0] out
);
assign out = in_sel[0] ? in_data_1 : in_data_0;
endmodule

module Register (
    input [15:0] I,
    output [15:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(16'h0000),
    .width(16)
) reg_P_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Mux2xOutSInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input S,
    output [15:0] O
);
commonlib_muxn__N2__width16 coreir_commonlib_mux2x16_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(O)
);
endmodule

module Test2 (
    input sel,
    output [15:0] O,
    input CLK
);
wire [15:0] Register_inst0_O;
Mux2xOutSInt16 Mux2xOutSInt16_inst0 (
    .I0(Register_inst0_O),
    .I1(16'(Register_inst0_O + 16'h0001)),
    .S(sel),
    .O(O)
);
Register Register_inst0 (
    .I(O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
endmodule


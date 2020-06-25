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

module commonlib_muxn__N2__width8 (
    input [7:0] in_data_0,
    input [7:0] in_data_1,
    input [0:0] in_sel,
    output [7:0] out
);
assign out = in_sel[0] ? in_data_1 : in_data_0;
endmodule

module Mux2xTuplex_OutUInt8 (
    input [7:0] I0_x,
    input [7:0] I1_x,
    output [7:0] O_x,
    input S
);
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data_0(I0_x),
    .in_data_1(I1_x),
    .in_sel(S),
    .out(O_x)
);
endmodule

module Test_comb (
    output [7:0] O0_x,
    output [7:0] O1_a_x,
    input c,
    input [7:0] self_a_O_x
);
Mux2xTuplex_OutUInt8 Mux2xTuplex_OutUInt8_inst0 (
    .I0_x(self_a_O_x),
    .I1_x(self_a_O_x + 8'h01),
    .O_x(O1_a_x),
    .S(c)
);
assign O0_x = self_a_O_x;
endmodule

module Test (
    input CLK,
    output [7:0] O_a_x,
    input c
);
wire [7:0] Test_comb_inst0_O0_x;
wire [7:0] reg_P_inst0_out;
Test_comb Test_comb_inst0 (
    .O0_x(Test_comb_inst0_O0_x),
    .O1_a_x(O_a_x),
    .c(c),
    .self_a_O_x(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(CLK),
    .in(Test_comb_inst0_O0_x),
    .out(reg_P_inst0_out)
);
endmodule


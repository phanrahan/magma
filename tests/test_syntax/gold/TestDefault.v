module coreir_reg_arst #(
    parameter width = 1,
    parameter arst_posedge = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input arst,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg;
  wire real_rst;
  assign real_rst = arst_posedge ? arst : ~arst;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk, posedge real_rst) begin
    if (real_rst) outReg <= init;
    else outReg <= in;
  end
  assign out = outReg;
endmodule

module coreir_lshr #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 >> in1;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module TestDefault_comb (
    input [2:0] index,
    input [7:0] self_x_O,
    output [7:0] O0,
    output O1
);
wire bit_const_0_None_out;
wire [7:0] magma_Bits_8_lshr_inst0_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
wire [7:0] magma_Bits_8_lshr_inst0_in1;
assign magma_Bits_8_lshr_inst0_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,index[2:0]};
coreir_lshr #(
    .width(8)
) magma_Bits_8_lshr_inst0 (
    .in0(self_x_O),
    .in1(magma_Bits_8_lshr_inst0_in1),
    .out(magma_Bits_8_lshr_inst0_out)
);
assign O0 = self_x_O;
assign O1 = magma_Bits_8_lshr_inst0_out[0];
endmodule

module TestDefault (
    input [2:0] index,
    input CLK,
    input ASYNCRESET,
    output O
);
wire [7:0] TestDefault_comb_inst0_O0;
wire TestDefault_comb_inst0_O1;
wire [7:0] reg_PR_inst0_out;
TestDefault_comb TestDefault_comb_inst0 (
    .index(index),
    .self_x_O(reg_PR_inst0_out),
    .O0(TestDefault_comb_inst0_O0),
    .O1(TestDefault_comb_inst0_O1)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(8'hfe),
    .width(8)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestDefault_comb_inst0_O0),
    .out(reg_PR_inst0_out)
);
assign O = TestDefault_comb_inst0_O1;
endmodule


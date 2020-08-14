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

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module TestCall_comb (
    input [1:0] I,
    input [1:0] self_x_O,
    input [2:0] self_y_O,
    output [1:0] O0,
    output [2:0] O1,
    output [2:0] O2
);
wire bit_const_0_None_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
assign O0 = I;
assign O1 = {bit_const_0_None_out,self_x_O[1:0]};
assign O2 = self_y_O;
endmodule

module TestCall (
    input [1:0] I,
    input CLK,
    input ASYNCRESET,
    output [2:0] O
);
wire [1:0] TestCall_comb_inst0_O0;
wire [2:0] TestCall_comb_inst0_O1;
wire [2:0] TestCall_comb_inst0_O2;
wire [1:0] reg_PR_inst0_out;
wire [2:0] reg_PR_inst1_out;
TestCall_comb TestCall_comb_inst0 (
    .I(I),
    .self_x_O(reg_PR_inst0_out),
    .self_y_O(reg_PR_inst1_out),
    .O0(TestCall_comb_inst0_O0),
    .O1(TestCall_comb_inst0_O1),
    .O2(TestCall_comb_inst0_O2)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestCall_comb_inst0_O0),
    .out(reg_PR_inst0_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_PR_inst1 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestCall_comb_inst0_O1),
    .out(reg_PR_inst1_out)
);
assign O = TestCall_comb_inst0_O2;
endmodule


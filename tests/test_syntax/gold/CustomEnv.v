module coreir_reg_arst #(parameter width = 1, parameter arst_posedge = 1, parameter clk_posedge = 1, parameter init = 1) (input clk, input arst, input [width-1:0] in, output [width-1:0] out);
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

module TestBasic_comb (input [1:0] I, output [1:0] O0, output [1:0] O1, output [1:0] O2, input [1:0] self_x_O, input [1:0] self_y_O);
assign O0 = I;
assign O1 = self_x_O;
assign O2 = self_y_O;
endmodule

module TestBasic (input ASYNCRESET, input CLK, input [1:0] I, output [1:0] O);
wire [1:0] TestBasic_comb_inst0_O0;
wire [1:0] TestBasic_comb_inst0_O1;
wire [1:0] TestBasic_comb_inst0_O2;
wire [1:0] reg_PR_inst0_out;
wire [1:0] reg_PR_inst1_out;
TestBasic_comb TestBasic_comb_inst0(.I(I), .O0(TestBasic_comb_inst0_O0), .O1(TestBasic_comb_inst0_O1), .O2(TestBasic_comb_inst0_O2), .self_x_O(reg_PR_inst0_out), .self_y_O(reg_PR_inst1_out));
coreir_reg_arst #(.arst_posedge(1'b1), .clk_posedge(1'b1), .init(2'h2), .width(2)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(TestBasic_comb_inst0_O0), .out(reg_PR_inst0_out));
coreir_reg_arst #(.arst_posedge(1'b1), .clk_posedge(1'b1), .init(2'h0), .width(2)) reg_PR_inst1(.arst(ASYNCRESET), .clk(CLK), .in(TestBasic_comb_inst0_O1), .out(reg_PR_inst1_out));
assign O = TestBasic_comb_inst0_O2;
endmodule


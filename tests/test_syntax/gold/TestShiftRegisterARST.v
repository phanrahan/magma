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

module TestShiftRegister_comb (input [1:0] I, output [1:0] O0, output [1:0] O1, output [1:0] O2, input [1:0] self_x_O, input [1:0] self_y_O);
assign O0 = I;
assign O1 = self_x_O;
assign O2 = self_y_O;
endmodule

module CustomRegister_comb (input [1:0] I, output [1:0] O0, output [1:0] O1, input [1:0] self_value_O);
assign O0 = I;
assign O1 = self_value_O;
endmodule

module CustomRegister_unq1 (input ASYNCRESET, input CLK, input [1:0] I, output [1:0] O);
wire [1:0] CustomRegister_comb_inst0_O0;
wire [1:0] CustomRegister_comb_inst0_O1;
wire [1:0] reg_PR_inst0_out;
CustomRegister_comb CustomRegister_comb_inst0(.I(I), .O0(CustomRegister_comb_inst0_O0), .O1(CustomRegister_comb_inst0_O1), .self_value_O(reg_PR_inst0_out));
coreir_reg_arst #(.arst_posedge(1), .clk_posedge(1), .init(2'h1), .width(2)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(CustomRegister_comb_inst0_O0), .out(reg_PR_inst0_out));
assign O = CustomRegister_comb_inst0_O1;
endmodule

module CustomRegister (input ASYNCRESET, input CLK, input [1:0] I, output [1:0] O);
wire [1:0] CustomRegister_comb_inst0_O0;
wire [1:0] CustomRegister_comb_inst0_O1;
wire [1:0] reg_PR_inst0_out;
CustomRegister_comb CustomRegister_comb_inst0(.I(I), .O0(CustomRegister_comb_inst0_O0), .O1(CustomRegister_comb_inst0_O1), .self_value_O(reg_PR_inst0_out));
coreir_reg_arst #(.arst_posedge(1), .clk_posedge(1), .init(2'h0), .width(2)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(CustomRegister_comb_inst0_O0), .out(reg_PR_inst0_out));
assign O = CustomRegister_comb_inst0_O1;
endmodule

module TestShiftRegister (input ASYNCRESET, input CLK, input [1:0] I, output [1:0] O);
wire [1:0] CustomRegister_inst0_O;
wire [1:0] CustomRegister_inst1_O;
wire [1:0] TestShiftRegister_comb_inst0_O0;
wire [1:0] TestShiftRegister_comb_inst0_O1;
wire [1:0] TestShiftRegister_comb_inst0_O2;
CustomRegister CustomRegister_inst0(.ASYNCRESET(ASYNCRESET), .CLK(CLK), .I(TestShiftRegister_comb_inst0_O0), .O(CustomRegister_inst0_O));
CustomRegister_unq1 CustomRegister_inst1(.ASYNCRESET(ASYNCRESET), .CLK(CLK), .I(TestShiftRegister_comb_inst0_O1), .O(CustomRegister_inst1_O));
TestShiftRegister_comb TestShiftRegister_comb_inst0(.I(I), .O0(TestShiftRegister_comb_inst0_O0), .O1(TestShiftRegister_comb_inst0_O1), .O2(TestShiftRegister_comb_inst0_O2), .self_x_O(CustomRegister_inst0_O), .self_y_O(CustomRegister_inst1_O));
assign O = TestShiftRegister_comb_inst0_O2;
endmodule


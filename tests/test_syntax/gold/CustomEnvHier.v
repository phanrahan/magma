module coreir_reg #(parameter width = 1, parameter clk_posedge = 1, parameter init = 1) (input clk, input [width-1:0] in, output [width-1:0] out);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module TestBasic_comb (input [1:0] I, output [1:0] O0, output [1:0] O1, output [1:0] O2, input [1:0] self_x_O, input [1:0] self_y_O);
assign O0 = I;
assign O1 = self_x_O;
assign O2 = self_y_O;
endmodule

module Register_comb (input [1:0] I, output [1:0] O0, output [1:0] O1, input [1:0] self_value_O);
assign O0 = I;
assign O1 = self_value_O;
endmodule

module Register (input CLK, input [1:0] I, output [1:0] O);
wire [1:0] Register_comb_inst0_O0;
wire [1:0] Register_comb_inst0_O1;
wire [1:0] reg_P_inst0_out;
Register_comb Register_comb_inst0(.I(I), .O0(Register_comb_inst0_O0), .O1(Register_comb_inst0_O1), .self_value_O(reg_P_inst0_out));
coreir_reg #(.clk_posedge(1), .init(2'h0), .width(2)) reg_P_inst0(.clk(CLK), .in(Register_comb_inst0_O0), .out(reg_P_inst0_out));
assign O = Register_comb_inst0_O1;
endmodule

module TestBasic (input CLK, input [1:0] I, output [1:0] O);
wire [1:0] Register_inst0_O;
wire [1:0] TestBasic_comb_inst0_O0;
wire [1:0] TestBasic_comb_inst0_O1;
wire [1:0] TestBasic_comb_inst0_O2;
wire [1:0] reg_P_inst0_out;
Register Register_inst0(.CLK(CLK), .I(TestBasic_comb_inst0_O1), .O(Register_inst0_O));
TestBasic_comb TestBasic_comb_inst0(.I(I), .O0(TestBasic_comb_inst0_O0), .O1(TestBasic_comb_inst0_O1), .O2(TestBasic_comb_inst0_O2), .self_x_O(reg_P_inst0_out), .self_y_O(Register_inst0_O));
coreir_reg #(.clk_posedge(1), .init(2'h2), .width(2)) reg_P_inst0(.clk(CLK), .in(TestBasic_comb_inst0_O0), .out(reg_P_inst0_out));
assign O = TestBasic_comb_inst0_O2;
endmodule


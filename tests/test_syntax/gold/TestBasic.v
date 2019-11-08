module coreir_reg #(parameter width = 1, parameter clk_posedge = 1, parameter init = 1) (input clk, input [width-1:0] in, output [width-1:0] out);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module TestBasic_comb (input [1:0] I, output [1:0] O0, output [1:0] O1, output O2, output [1:0] O3, input [1:0] self_x_O, input [1:0] self_y_O, input self_z_O);
assign O0 = I;
assign O1 = self_x_O;
assign O2 = self_z_O;
assign O3 = self_y_O;
endmodule

module DFF_init0_has_ceFalse_has_resetFalse_has_async_resetFalse (input CLK, input I, output O);
wire [0:0] reg_P_inst0_out;
coreir_reg #(.clk_posedge(1), .init(1'h0), .width(1)) reg_P_inst0(.clk(CLK), .in(I), .out(reg_P_inst0_out));
assign O = reg_P_inst0_out[0];
endmodule

module TestBasic (input CLK, input [1:0] I, output [1:0] O);
wire DFF_init0_has_ceFalse_has_resetFalse_has_async_resetFalse_inst0_O;
wire [1:0] TestBasic_comb_inst0_O0;
wire [1:0] TestBasic_comb_inst0_O1;
wire TestBasic_comb_inst0_O2;
wire [1:0] TestBasic_comb_inst0_O3;
wire [1:0] reg_P_inst0_out;
wire [1:0] reg_P_inst1_out;
DFF_init0_has_ceFalse_has_resetFalse_has_async_resetFalse DFF_init0_has_ceFalse_has_resetFalse_has_async_resetFalse_inst0(.CLK(CLK), .I(TestBasic_comb_inst0_O2), .O(DFF_init0_has_ceFalse_has_resetFalse_has_async_resetFalse_inst0_O));
TestBasic_comb TestBasic_comb_inst0(.I(I), .O0(TestBasic_comb_inst0_O0), .O1(TestBasic_comb_inst0_O1), .O2(TestBasic_comb_inst0_O2), .O3(TestBasic_comb_inst0_O3), .self_x_O(reg_P_inst0_out), .self_y_O(reg_P_inst1_out), .self_z_O(DFF_init0_has_ceFalse_has_resetFalse_has_async_resetFalse_inst0_O));
coreir_reg #(.clk_posedge(1), .init(2'h0), .width(2)) reg_P_inst0(.clk(CLK), .in(TestBasic_comb_inst0_O0), .out(reg_P_inst0_out));
coreir_reg #(.clk_posedge(1), .init(2'h0), .width(2)) reg_P_inst1(.clk(CLK), .in(TestBasic_comb_inst0_O1), .out(reg_P_inst1_out));
assign O = TestBasic_comb_inst0_O3;
endmodule


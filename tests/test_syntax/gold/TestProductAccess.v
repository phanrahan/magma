// Module `Mux2xTuplea0_OutBits8_a1_OutBits8` defined externally
module coreir_reg #(parameter width = 1, parameter clk_posedge = 1, parameter init = 1) (input clk, input [width-1:0] in, output [width-1:0] out);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module TestProductAccess_comb (output [7:0] O0_a0, output [7:0] O0_a1, output [7:0] O1_a0, output [7:0] O1_a1, input sel, input [7:0] self_a_O_a0, input [7:0] self_a_O_a1, input [7:0] value);
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
Mux2xTuplea0_OutBits8_a1_OutBits8 Mux2xTuplea0_OutBits8_a1_OutBits8_inst0(.I0_a0(self_a_O_a0), .I0_a1(value), .I1_a0(value), .I1_a1(self_a_O_a1), .O_a0(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0), .O_a1(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1), .S(sel));
assign O0_a0 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
assign O0_a1 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
assign O1_a0 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
assign O1_a1 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
endmodule

module TestProductAccess (input CLK, output [7:0] O_a0, output [7:0] O_a1, input sel, input [7:0] value);
wire [7:0] TestProductAccess_comb_inst0_O0_a0;
wire [7:0] TestProductAccess_comb_inst0_O0_a1;
wire [7:0] TestProductAccess_comb_inst0_O1_a0;
wire [7:0] TestProductAccess_comb_inst0_O1_a1;
wire [7:0] reg_P_inst0_out;
wire [7:0] reg_P_inst1_out;
TestProductAccess_comb TestProductAccess_comb_inst0(.O0_a0(TestProductAccess_comb_inst0_O0_a0), .O0_a1(TestProductAccess_comb_inst0_O0_a1), .O1_a0(TestProductAccess_comb_inst0_O1_a0), .O1_a1(TestProductAccess_comb_inst0_O1_a1), .sel(sel), .self_a_O_a0(reg_P_inst0_out), .self_a_O_a1(reg_P_inst1_out), .value(value));
coreir_reg #(.clk_posedge(1'b1), .init(8'h00), .width(8)) reg_P_inst0(.clk(CLK), .in(TestProductAccess_comb_inst0_O0_a0), .out(reg_P_inst0_out));
coreir_reg #(.clk_posedge(1'b1), .init(8'h00), .width(8)) reg_P_inst1(.clk(CLK), .in(TestProductAccess_comb_inst0_O0_a1), .out(reg_P_inst1_out));
assign O_a0 = TestProductAccess_comb_inst0_O1_a0;
assign O_a1 = TestProductAccess_comb_inst0_O1_a1;
endmodule


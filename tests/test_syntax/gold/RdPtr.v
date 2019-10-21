// Module `Mux2_x10` defined externally
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

module coreir_const #(parameter width = 1, parameter value = 1) (output [width-1:0] out);
  assign out = value;
endmodule

module coreir_add #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output [width-1:0] out);
  assign out = in0 + in1;
endmodule

module RdPtr_comb (output [9:0] O0, output [9:0] O1, input read, input [9:0] self_rd_ptr_O);
wire [9:0] Mux2_x10_inst0_O;
wire [9:0] const_1_10_out;
wire [9:0] magma_Bits_10_add_inst0_out;
Mux2_x10 Mux2_x10_inst0(.I0(self_rd_ptr_O), .I1(magma_Bits_10_add_inst0_out), .O(Mux2_x10_inst0_O), .S(read));
coreir_const #(.value(10'h001), .width(10)) const_1_10(.out(const_1_10_out));
coreir_add #(.width(10)) magma_Bits_10_add_inst0(.in0(self_rd_ptr_O), .in1(const_1_10_out), .out(magma_Bits_10_add_inst0_out));
assign O0 = Mux2_x10_inst0_O;
assign O1 = self_rd_ptr_O;
endmodule

module RdPtr (input ASYNCRESET, input CLK, output [9:0] O, input read);
wire [9:0] RdPtr_comb_inst0_O0;
wire [9:0] RdPtr_comb_inst0_O1;
wire [9:0] reg_PR_inst0_out;
RdPtr_comb RdPtr_comb_inst0(.O0(RdPtr_comb_inst0_O0), .O1(RdPtr_comb_inst0_O1), .read(read), .self_rd_ptr_O(reg_PR_inst0_out));
coreir_reg_arst #(.arst_posedge(1), .clk_posedge(1), .init(10'h000), .width(10)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(RdPtr_comb_inst0_O0), .out(reg_PR_inst0_out));
assign O = RdPtr_comb_inst0_O1;
endmodule


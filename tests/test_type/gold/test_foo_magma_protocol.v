module coreir_shl #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output [width-1:0] out);
  assign out = in0 << in1;
endmodule

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

module coreir_or #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output [width-1:0] out);
  assign out = in0 | in1;
endmodule

module coreir_const #(parameter width = 1, parameter value = 1) (output [width-1:0] out);
  assign out = value;
endmodule

module corebit_const #(parameter value = 1) (output out);
  assign out = value;
endmodule

module Bar_comb (output [0:0] O0, output [7:0] O1, input [7:0] foo, input [0:0] self_reg_O);
wire bit_const_0_None_out;
wire [7:0] const_1_8_out;
wire [7:0] const_2_8_out;
wire [7:0] magma_Bits_8_or_inst0_out;
wire [7:0] magma_Bits_8_or_inst1_out;
wire [7:0] magma_Bits_8_shl_inst0_out;
wire [7:0] magma_Bits_8_shl_inst1_out;
corebit_const #(.value(1'b0)) bit_const_0_None(.out(bit_const_0_None_out));
coreir_const #(.value(8'h01), .width(8)) const_1_8(.out(const_1_8_out));
coreir_const #(.value(8'h02), .width(8)) const_2_8(.out(const_2_8_out));
coreir_or #(.width(8)) magma_Bits_8_or_inst0(.in0(magma_Bits_8_shl_inst0_out), .in1(magma_Bits_8_shl_inst1_out), .out(magma_Bits_8_or_inst0_out));
coreir_or #(.width(8)) magma_Bits_8_or_inst1(.in0(magma_Bits_8_or_inst0_out), .in1({foo[0],bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out}), .out(magma_Bits_8_or_inst1_out));
coreir_shl #(.width(8)) magma_Bits_8_shl_inst0(.in0(foo), .in1(const_2_8_out), .out(magma_Bits_8_shl_inst0_out));
coreir_shl #(.width(8)) magma_Bits_8_shl_inst1(.in0({foo[0],bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out}), .in1(const_1_8_out), .out(magma_Bits_8_shl_inst1_out));
assign O0 = self_reg_O;
assign O1 = magma_Bits_8_or_inst1_out;
endmodule

module Bar (input ASYNCRESET, input CLK, output [7:0] O, input [7:0] foo);
wire [0:0] Bar_comb_inst0_O0;
wire [7:0] Bar_comb_inst0_O1;
wire [0:0] reg_PR_inst0_out;
Bar_comb Bar_comb_inst0(.O0(Bar_comb_inst0_O0), .O1(Bar_comb_inst0_O1), .foo(foo), .self_reg_O(reg_PR_inst0_out));
coreir_reg_arst #(.arst_posedge(1'b1), .clk_posedge(1'b1), .init(1'h0), .width(1)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(Bar_comb_inst0_O0), .out(reg_PR_inst0_out));
assign O = Bar_comb_inst0_O1;
endmodule


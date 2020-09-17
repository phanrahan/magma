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

module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module commonlib_muxn__N2__width10 (
    input [9:0] in_data [1:0],
    input [0:0] in_sel,
    output [9:0] out
);
wire [9:0] _join_out;
coreir_mux #(
    .width(10)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xUInt10 (
    input [9:0] I0,
    input [9:0] I1,
    input S,
    output [9:0] O
);
wire [9:0] coreir_commonlib_mux2x10_inst0_out;
wire [9:0] coreir_commonlib_mux2x10_inst0_in_data [1:0];
assign coreir_commonlib_mux2x10_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x10_inst0_in_data[0] = I0;
commonlib_muxn__N2__width10 coreir_commonlib_mux2x10_inst0 (
    .in_data(coreir_commonlib_mux2x10_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x10_inst0_out)
);
assign O = coreir_commonlib_mux2x10_inst0_out;
endmodule

module RdPtr_comb (
    input read,
    input [9:0] self_rd_ptr_O,
    output [9:0] O0,
    output [9:0] O1
);
wire [9:0] Mux2xUInt10_inst0_O;
wire [9:0] const_1_10_out;
wire [9:0] magma_Bits_10_add_inst0_out;
Mux2xUInt10 Mux2xUInt10_inst0 (
    .I0(self_rd_ptr_O),
    .I1(magma_Bits_10_add_inst0_out),
    .S(read),
    .O(Mux2xUInt10_inst0_O)
);
coreir_const #(
    .value(10'h001),
    .width(10)
) const_1_10 (
    .out(const_1_10_out)
);
coreir_add #(
    .width(10)
) magma_Bits_10_add_inst0 (
    .in0(self_rd_ptr_O),
    .in1(const_1_10_out),
    .out(magma_Bits_10_add_inst0_out)
);
assign O0 = Mux2xUInt10_inst0_O;
assign O1 = self_rd_ptr_O;
endmodule

module RdPtr (
    input read,
    input CLK,
    input ASYNCRESET,
    output [9:0] O
);
wire [9:0] RdPtr_comb_inst0_O0;
wire [9:0] RdPtr_comb_inst0_O1;
wire [9:0] reg_PR_inst0_out;
RdPtr_comb RdPtr_comb_inst0 (
    .read(read),
    .self_rd_ptr_O(reg_PR_inst0_out),
    .O0(RdPtr_comb_inst0_O0),
    .O1(RdPtr_comb_inst0_O1)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(10'h000),
    .width(10)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(RdPtr_comb_inst0_O0),
    .out(reg_PR_inst0_out)
);
assign O = RdPtr_comb_inst0_O1;
endmodule


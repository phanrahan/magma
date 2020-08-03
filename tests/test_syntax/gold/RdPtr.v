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
wire [9:0] _join_in0;
wire [9:0] _join_in1;
wire _join_sel;
wire [9:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(10)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutUInt10 (
    input [9:0] I0,
    input [9:0] I1,
    input S,
    output [9:0] O
);
wire [9:0] coreir_commonlib_mux2x10_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x10_inst0_in_sel;
wire [9:0] coreir_commonlib_mux2x10_inst0_out;
assign coreir_commonlib_mux2x10_inst0_in_data = '{I1,I0};
assign coreir_commonlib_mux2x10_inst0_in_sel = S;
commonlib_muxn__N2__width10 coreir_commonlib_mux2x10_inst0 (
    .in_data(coreir_commonlib_mux2x10_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x10_inst0_in_sel),
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
wire [9:0] Mux2xOutUInt10_inst0_I0;
wire [9:0] Mux2xOutUInt10_inst0_I1;
wire Mux2xOutUInt10_inst0_S;
wire [9:0] Mux2xOutUInt10_inst0_O;
wire [9:0] const_1_10_out;
wire [9:0] magma_Bits_10_add_inst0_in0;
wire [9:0] magma_Bits_10_add_inst0_in1;
wire [9:0] magma_Bits_10_add_inst0_out;
assign Mux2xOutUInt10_inst0_I0 = self_rd_ptr_O;
assign Mux2xOutUInt10_inst0_I1 = magma_Bits_10_add_inst0_out;
assign Mux2xOutUInt10_inst0_S = read;
Mux2xOutUInt10 Mux2xOutUInt10_inst0 (
    .I0(Mux2xOutUInt10_inst0_I0),
    .I1(Mux2xOutUInt10_inst0_I1),
    .S(Mux2xOutUInt10_inst0_S),
    .O(Mux2xOutUInt10_inst0_O)
);
coreir_const #(
    .value(10'h001),
    .width(10)
) const_1_10 (
    .out(const_1_10_out)
);
assign magma_Bits_10_add_inst0_in0 = self_rd_ptr_O;
assign magma_Bits_10_add_inst0_in1 = const_1_10_out;
coreir_add #(
    .width(10)
) magma_Bits_10_add_inst0 (
    .in0(magma_Bits_10_add_inst0_in0),
    .in1(magma_Bits_10_add_inst0_in1),
    .out(magma_Bits_10_add_inst0_out)
);
assign O0 = Mux2xOutUInt10_inst0_O;
assign O1 = self_rd_ptr_O;
endmodule

module RdPtr (
    input read,
    input CLK,
    input ASYNCRESET,
    output [9:0] O
);
wire RdPtr_comb_inst0_read;
wire [9:0] RdPtr_comb_inst0_self_rd_ptr_O;
wire [9:0] RdPtr_comb_inst0_O0;
wire [9:0] RdPtr_comb_inst0_O1;
wire reg_PR_inst0_clk;
wire reg_PR_inst0_arst;
wire [9:0] reg_PR_inst0_in;
wire [9:0] reg_PR_inst0_out;
assign RdPtr_comb_inst0_read = read;
assign RdPtr_comb_inst0_self_rd_ptr_O = reg_PR_inst0_out;
RdPtr_comb RdPtr_comb_inst0 (
    .read(RdPtr_comb_inst0_read),
    .self_rd_ptr_O(RdPtr_comb_inst0_self_rd_ptr_O),
    .O0(RdPtr_comb_inst0_O0),
    .O1(RdPtr_comb_inst0_O1)
);
assign reg_PR_inst0_clk = CLK;
assign reg_PR_inst0_arst = ASYNCRESET;
assign reg_PR_inst0_in = RdPtr_comb_inst0_O0;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(10'h000),
    .width(10)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
    .out(reg_PR_inst0_out)
);
assign O = RdPtr_comb_inst0_O1;
endmodule


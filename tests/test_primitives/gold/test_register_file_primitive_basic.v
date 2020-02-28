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

module commonlib_muxn__N2__width4 (
    input [3:0] in_data_0,
    input [3:0] in_data_1,
    input [0:0] in_sel,
    output [3:0] out
);
assign out = in_sel[0] ? in_data_1 : in_data_0;
endmodule

module commonlib_muxn__N4__width4 (
    input [3:0] in_data_0,
    input [3:0] in_data_1,
    input [3:0] in_data_2,
    input [3:0] in_data_3,
    input [1:0] in_sel,
    output [3:0] out
);
wire [3:0] muxN_0_out;
wire [3:0] muxN_1_out;
commonlib_muxn__N2__width4 muxN_0 (
    .in_data_0(in_data_0),
    .in_data_1(in_data_1),
    .in_sel(in_sel[1 - 1:0]),
    .out(muxN_0_out)
);
commonlib_muxn__N2__width4 muxN_1 (
    .in_data_0(in_data_2),
    .in_data_1(in_data_3),
    .in_sel(in_sel[1 - 1:0]),
    .out(muxN_1_out)
);
assign out = in_sel[1] ? muxN_1_out : muxN_0_out;
endmodule

module Mux_unq1 (
    input [3:0] I0,
    input [3:0] I1,
    input [0:0] S,
    output [3:0] O
);
commonlib_muxn__N2__width4 coreir_commonlib_mux2x4_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(O)
);
endmodule

module Mux (
    input [3:0] I0,
    input [3:0] I1,
    input [3:0] I2,
    input [3:0] I3,
    input [1:0] S,
    output [3:0] O
);
commonlib_muxn__N4__width4 coreir_commonlib_mux4x4_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_data_2(I2),
    .in_data_3(I3),
    .in_sel(S),
    .out(O)
);
endmodule

module StagedCircuit (
    input ASYNCRESET,
    input CLK,
    input [1:0] read_0_addr,
    output [3:0] read_0_data,
    input [1:0] write_0_addr,
    input [3:0] write_0_data
);
wire [3:0] Mux_inst0_O;
wire [3:0] Mux_inst1_O;
wire [3:0] Mux_inst2_O;
wire [3:0] Mux_inst3_O;
wire [3:0] Mux_inst4_O;
wire [3:0] reg_PR_inst0_out;
wire [3:0] reg_PR_inst1_out;
wire [3:0] reg_PR_inst2_out;
wire [3:0] reg_PR_inst3_out;
Mux Mux_inst0 (
    .I0(reg_PR_inst0_out),
    .I1(reg_PR_inst1_out),
    .I2(reg_PR_inst2_out),
    .I3(reg_PR_inst3_out),
    .S(read_0_addr),
    .O(Mux_inst0_O)
);
Mux_unq1 Mux_inst1 (
    .I0(write_0_data),
    .I1(reg_PR_inst0_out),
    .S(write_0_addr == 2'h0),
    .O(Mux_inst1_O)
);
Mux_unq1 Mux_inst2 (
    .I0(write_0_data),
    .I1(reg_PR_inst1_out),
    .S(write_0_addr == 2'h1),
    .O(Mux_inst2_O)
);
Mux_unq1 Mux_inst3 (
    .I0(write_0_data),
    .I1(reg_PR_inst2_out),
    .S(write_0_addr == 2'h2),
    .O(Mux_inst3_O)
);
Mux_unq1 Mux_inst4 (
    .I0(write_0_data),
    .I1(reg_PR_inst3_out),
    .S(write_0_addr == 2'h3),
    .O(Mux_inst4_O)
);
Mux_unq1 Mux_inst5 (
    .I0(write_0_data),
    .I1(Mux_inst0_O),
    .S(write_0_addr == read_0_addr),
    .O(read_0_data)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(Mux_inst1_O),
    .out(reg_PR_inst0_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_PR_inst1 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(Mux_inst2_O),
    .out(reg_PR_inst1_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_PR_inst2 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(Mux_inst3_O),
    .out(reg_PR_inst2_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_PR_inst3 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(Mux_inst4_O),
    .out(reg_PR_inst3_out)
);
endmodule

module Main (
    input [1:0] write_addr,
    input [3:0] write_data,
    input [1:0] read_addr,
    output [3:0] read_data,
    input CLK,
    input ASYNCRESET
);
StagedCircuit StagedCircuit_inst0 (
    .ASYNCRESET(ASYNCRESET),
    .CLK(CLK),
    .read_0_addr(read_addr),
    .read_0_data(read_data),
    .write_0_addr(write_addr),
    .write_0_data(write_data)
);
endmodule


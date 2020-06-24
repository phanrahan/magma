module coreir_reg #(
    parameter width = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
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

module commonlib_muxn__N2__width24 (
    input [23:0] in_data_0,
    input [23:0] in_data_1,
    input [0:0] in_sel,
    output [23:0] out
);
wire [23:0] _join_out;
coreir_mux #(
    .width(24)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xArray3_Bits8 (
    input [7:0] I0_0,
    input [7:0] I0_1,
    input [7:0] I0_2,
    input [7:0] I1_0,
    input [7:0] I1_1,
    input [7:0] I1_2,
    output [7:0] O_0,
    output [7:0] O_1,
    output [7:0] O_2,
    input S
);
wire [23:0] coreir_commonlib_mux2x24_inst0_out;
commonlib_muxn__N2__width24 coreir_commonlib_mux2x24_inst0 (
    .in_data_0({I0_2[7:0],I0_1[7:0],I0_0[7:0]}),
    .in_data_1({I1_2[7:0],I1_1[7:0],I1_0[7:0]}),
    .in_sel(S),
    .out(coreir_commonlib_mux2x24_inst0_out)
);
assign O_0 = coreir_commonlib_mux2x24_inst0_out[7:0];
assign O_1 = coreir_commonlib_mux2x24_inst0_out[15:8];
assign O_2 = coreir_commonlib_mux2x24_inst0_out[23:16];
endmodule

module Register (
    input CLK,
    input [7:0] I_0,
    input [7:0] I_1,
    input [7:0] I_2,
    output [7:0] O_0,
    output [7:0] O_1,
    output [7:0] O_2,
    input RESET
);
wire [7:0] Mux2xArray3_Bits8_inst0_O_0;
wire [7:0] Mux2xArray3_Bits8_inst0_O_1;
wire [7:0] Mux2xArray3_Bits8_inst0_O_2;
wire [7:0] const_173_8_out;
wire [7:0] const_190_8_out;
wire [7:0] const_222_8_out;
wire [23:0] reg_P_inst0_out;
Mux2xArray3_Bits8 Mux2xArray3_Bits8_inst0 (
    .I0_0(I_0),
    .I0_1(I_1),
    .I0_2(I_2),
    .I1_0(const_222_8_out),
    .I1_1(const_173_8_out),
    .I1_2(const_190_8_out),
    .O_0(Mux2xArray3_Bits8_inst0_O_0),
    .O_1(Mux2xArray3_Bits8_inst0_O_1),
    .O_2(Mux2xArray3_Bits8_inst0_O_2),
    .S(RESET)
);
coreir_const #(
    .value(8'had),
    .width(8)
) const_173_8 (
    .out(const_173_8_out)
);
coreir_const #(
    .value(8'hbe),
    .width(8)
) const_190_8 (
    .out(const_190_8_out)
);
coreir_const #(
    .value(8'hde),
    .width(8)
) const_222_8 (
    .out(const_222_8_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'h000000),
    .width(24)
) reg_P_inst0 (
    .clk(CLK),
    .in({Mux2xArray3_Bits8_inst0_O_2[7:0],Mux2xArray3_Bits8_inst0_O_1[7:0],Mux2xArray3_Bits8_inst0_O_0[7:0]}),
    .out(reg_P_inst0_out)
);
assign O_0 = reg_P_inst0_out[7:0];
assign O_1 = reg_P_inst0_out[15:8];
assign O_2 = reg_P_inst0_out[23:16];
endmodule

module test_reg_of_nested_array (
    input CLK,
    input [7:0] I_0,
    input [7:0] I_1,
    input [7:0] I_2,
    output [7:0] O_0,
    output [7:0] O_1,
    output [7:0] O_2,
    input RESET
);
wire [7:0] Register_inst0_O_0;
wire [7:0] Register_inst0_O_1;
wire [7:0] Register_inst0_O_2;
Register Register_inst0 (
    .CLK(CLK),
    .I_0(I_0),
    .I_1(I_1),
    .I_2(I_2),
    .O_0(Register_inst0_O_0),
    .O_1(Register_inst0_O_1),
    .O_2(Register_inst0_O_2),
    .RESET(RESET)
);
assign O_0 = Register_inst0_O_0;
assign O_1 = Register_inst0_O_1;
assign O_2 = Register_inst0_O_2;
endmodule


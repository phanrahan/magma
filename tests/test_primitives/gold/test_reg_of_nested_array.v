module mantle_wire__typeBitIn24 (
    output [23:0] in,
    input [23:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit24 (
    input [23:0] in,
    output [23:0] out
);
assign out = in;
endmodule

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
    input [23:0] in_data [1:0],
    input [0:0] in_sel,
    output [23:0] out
);
wire [23:0] _join_in0;
wire [23:0] _join_in1;
wire _join_sel;
wire [23:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(24)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xArray3_Bits8 (
    input [7:0] I0 [2:0],
    input [7:0] I1 [2:0],
    input S,
    output [7:0] O [2:0]
);
wire [23:0] _$_U2_in;
wire [23:0] _$_U2_out;
wire [23:0] _$_U3_in;
wire [23:0] _$_U3_out;
wire [23:0] _$_U4_in;
wire [23:0] _$_U4_out;
wire [23:0] coreir_commonlib_mux2x24_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x24_inst0_in_sel;
wire [23:0] coreir_commonlib_mux2x24_inst0_out;
assign _$_U2_out = {I0[2][7:0],I0[1][7:0],I0[0][7:0]};
mantle_wire__typeBitIn24 _$_U2 (
    .in(_$_U2_in),
    .out(_$_U2_out)
);
assign _$_U3_out = {I1[2][7:0],I1[1][7:0],I1[0][7:0]};
mantle_wire__typeBitIn24 _$_U3 (
    .in(_$_U3_in),
    .out(_$_U3_out)
);
assign _$_U4_in = coreir_commonlib_mux2x24_inst0_out;
mantle_wire__typeBit24 _$_U4 (
    .in(_$_U4_in),
    .out(_$_U4_out)
);
assign coreir_commonlib_mux2x24_inst0_in_data = '{_$_U3_in,_$_U2_in};
assign coreir_commonlib_mux2x24_inst0_in_sel = S;
commonlib_muxn__N2__width24 coreir_commonlib_mux2x24_inst0 (
    .in_data(coreir_commonlib_mux2x24_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x24_inst0_in_sel),
    .out(coreir_commonlib_mux2x24_inst0_out)
);
assign O = '{_$_U4_out[23:16],_$_U4_out[15:8],_$_U4_out[7:0]};
endmodule

module Register (
    input [7:0] I [2:0],
    output [7:0] O [2:0],
    input CLK,
    input RESET
);
wire [7:0] Mux2xArray3_Bits8_inst0_I0 [2:0];
wire [7:0] Mux2xArray3_Bits8_inst0_I1 [2:0];
wire Mux2xArray3_Bits8_inst0_S;
wire [7:0] Mux2xArray3_Bits8_inst0_O [2:0];
wire [7:0] const_173_8_out;
wire [7:0] const_190_8_out;
wire [7:0] const_222_8_out;
wire reg_P_inst0_clk;
wire [23:0] reg_P_inst0_in;
wire [23:0] reg_P_inst0_out;
assign Mux2xArray3_Bits8_inst0_I0 = '{I[2],I[1],I[0]};
assign Mux2xArray3_Bits8_inst0_I1 = '{const_190_8_out,const_173_8_out,const_222_8_out};
assign Mux2xArray3_Bits8_inst0_S = RESET;
Mux2xArray3_Bits8 Mux2xArray3_Bits8_inst0 (
    .I0(Mux2xArray3_Bits8_inst0_I0),
    .I1(Mux2xArray3_Bits8_inst0_I1),
    .S(Mux2xArray3_Bits8_inst0_S),
    .O(Mux2xArray3_Bits8_inst0_O)
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
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = {Mux2xArray3_Bits8_inst0_O[2][7:0],Mux2xArray3_Bits8_inst0_O[1][7:0],Mux2xArray3_Bits8_inst0_O[0][7:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'h000000),
    .width(24)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O = '{reg_P_inst0_out[23:16],reg_P_inst0_out[15:8],reg_P_inst0_out[7:0]};
endmodule

module test_reg_of_nested_array (
    input [7:0] I [2:0],
    output [7:0] O [2:0],
    input CLK,
    input RESET
);
wire [7:0] Register_inst0_I [2:0];
wire [7:0] Register_inst0_O [2:0];
wire Register_inst0_CLK;
wire Register_inst0_RESET;
assign Register_inst0_I = '{I[2],I[1],I[0]};
assign Register_inst0_CLK = CLK;
assign Register_inst0_RESET = RESET;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK),
    .RESET(Register_inst0_RESET)
);
assign O = '{Register_inst0_O[2],Register_inst0_O[1],Register_inst0_O[0]};
endmodule


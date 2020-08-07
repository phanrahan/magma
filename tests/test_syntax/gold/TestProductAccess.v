module mantle_wire__typeBitIn8 (
    output [7:0] in,
    input [7:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn16 (
    output [15:0] in,
    input [15:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit8 (
    input [7:0] in,
    output [7:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit16 (
    input [15:0] in,
    output [15:0] out
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

module commonlib_muxn__N2__width16 (
    input [15:0] in_data [1:0],
    input [0:0] in_sel,
    output [15:0] out
);
wire [15:0] _join_in0;
wire [15:0] _join_in1;
wire _join_sel;
wire [15:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(16)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTuplea0_OutBits8_a1_OutBits8 (
    input [7:0] I0_a0,
    input [7:0] I0_a1,
    input [7:0] I1_a0,
    input [7:0] I1_a1,
    output [7:0] O_a0,
    output [7:0] O_a1,
    input S
);
wire [7:0] _$_U10_in;
wire [7:0] _$_U10_out;
wire [7:0] _$_U11_in;
wire [7:0] _$_U11_out;
wire [15:0] _$_U2_in;
wire [15:0] _$_U2_out;
wire [15:0] _$_U3_in;
wire [15:0] _$_U3_out;
wire [15:0] _$_U4_in;
wire [15:0] _$_U4_out;
wire [7:0] _$_U6_in;
wire [7:0] _$_U6_out;
wire [7:0] _$_U7_in;
wire [7:0] _$_U7_out;
wire [7:0] _$_U8_in;
wire [7:0] _$_U8_out;
wire [7:0] _$_U9_in;
wire [7:0] _$_U9_out;
wire [15:0] coreir_commonlib_mux2x16_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x16_inst0_in_sel;
wire [15:0] coreir_commonlib_mux2x16_inst0_out;
assign _$_U10_out = _$_U4_out[7:0];
mantle_wire__typeBitIn8 _$_U10 (
    .in(_$_U10_in),
    .out(_$_U10_out)
);
assign _$_U11_out = _$_U4_out[15:8];
mantle_wire__typeBitIn8 _$_U11 (
    .in(_$_U11_in),
    .out(_$_U11_out)
);
assign _$_U2_out = {_$_U7_out[7:0],_$_U6_out[7:0]};
mantle_wire__typeBitIn16 _$_U2 (
    .in(_$_U2_in),
    .out(_$_U2_out)
);
assign _$_U3_out = {_$_U9_out[7:0],_$_U8_out[7:0]};
mantle_wire__typeBitIn16 _$_U3 (
    .in(_$_U3_in),
    .out(_$_U3_out)
);
assign _$_U4_in = coreir_commonlib_mux2x16_inst0_out;
mantle_wire__typeBit16 _$_U4 (
    .in(_$_U4_in),
    .out(_$_U4_out)
);
assign _$_U6_in = I0_a0;
mantle_wire__typeBit8 _$_U6 (
    .in(_$_U6_in),
    .out(_$_U6_out)
);
assign _$_U7_in = I0_a1;
mantle_wire__typeBit8 _$_U7 (
    .in(_$_U7_in),
    .out(_$_U7_out)
);
assign _$_U8_in = I1_a0;
mantle_wire__typeBit8 _$_U8 (
    .in(_$_U8_in),
    .out(_$_U8_out)
);
assign _$_U9_in = I1_a1;
mantle_wire__typeBit8 _$_U9 (
    .in(_$_U9_in),
    .out(_$_U9_out)
);
assign coreir_commonlib_mux2x16_inst0_in_data[1] = _$_U3_in;
assign coreir_commonlib_mux2x16_inst0_in_data[0] = _$_U2_in;
assign coreir_commonlib_mux2x16_inst0_in_sel[0] = S;
commonlib_muxn__N2__width16 coreir_commonlib_mux2x16_inst0 (
    .in_data(coreir_commonlib_mux2x16_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x16_inst0_in_sel),
    .out(coreir_commonlib_mux2x16_inst0_out)
);
assign O_a0 = _$_U10_in;
assign O_a1 = _$_U11_in;
endmodule

module TestProductAccess_comb (
    output [7:0] O0_a0,
    output [7:0] O0_a1,
    output [7:0] O1_a0,
    output [7:0] O1_a1,
    input sel,
    input [7:0] self_a_O_a0,
    input [7:0] self_a_O_a1,
    input [7:0] value
);
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I0_a0;
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I0_a1;
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I1_a0;
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I1_a1;
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
wire Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_S;
assign Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I0_a0 = self_a_O_a0;
assign Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I0_a1 = value;
assign Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I1_a0 = value;
assign Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I1_a1 = self_a_O_a1;
assign Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_S = sel;
Mux2xTuplea0_OutBits8_a1_OutBits8 Mux2xTuplea0_OutBits8_a1_OutBits8_inst0 (
    .I0_a0(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I0_a0),
    .I0_a1(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I0_a1),
    .I1_a0(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I1_a0),
    .I1_a1(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_I1_a1),
    .O_a0(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0),
    .O_a1(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1),
    .S(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_S)
);
assign O0_a0 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
assign O0_a1 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
assign O1_a0 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
assign O1_a1 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
endmodule

module TestProductAccess (
    input CLK,
    output [7:0] O_a0,
    output [7:0] O_a1,
    input sel,
    input [7:0] value
);
wire [7:0] TestProductAccess_comb_inst0_O0_a0;
wire [7:0] TestProductAccess_comb_inst0_O0_a1;
wire [7:0] TestProductAccess_comb_inst0_O1_a0;
wire [7:0] TestProductAccess_comb_inst0_O1_a1;
wire TestProductAccess_comb_inst0_sel;
wire [7:0] TestProductAccess_comb_inst0_self_a_O_a0;
wire [7:0] TestProductAccess_comb_inst0_self_a_O_a1;
wire [7:0] TestProductAccess_comb_inst0_value;
wire reg_P_inst0_clk;
wire [7:0] reg_P_inst0_in;
wire [7:0] reg_P_inst0_out;
wire reg_P_inst1_clk;
wire [7:0] reg_P_inst1_in;
wire [7:0] reg_P_inst1_out;
assign TestProductAccess_comb_inst0_sel = sel;
assign TestProductAccess_comb_inst0_self_a_O_a0 = reg_P_inst0_out;
assign TestProductAccess_comb_inst0_self_a_O_a1 = reg_P_inst1_out;
assign TestProductAccess_comb_inst0_value = value;
TestProductAccess_comb TestProductAccess_comb_inst0 (
    .O0_a0(TestProductAccess_comb_inst0_O0_a0),
    .O0_a1(TestProductAccess_comb_inst0_O0_a1),
    .O1_a0(TestProductAccess_comb_inst0_O1_a0),
    .O1_a1(TestProductAccess_comb_inst0_O1_a1),
    .sel(TestProductAccess_comb_inst0_sel),
    .self_a_O_a0(TestProductAccess_comb_inst0_self_a_O_a0),
    .self_a_O_a1(TestProductAccess_comb_inst0_self_a_O_a1),
    .value(TestProductAccess_comb_inst0_value)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = TestProductAccess_comb_inst0_O0_a0;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign reg_P_inst1_clk = CLK;
assign reg_P_inst1_in = TestProductAccess_comb_inst0_O0_a1;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst1 (
    .clk(reg_P_inst1_clk),
    .in(reg_P_inst1_in),
    .out(reg_P_inst1_out)
);
assign O_a0 = TestProductAccess_comb_inst0_O1_a0;
assign O_a1 = TestProductAccess_comb_inst0_O1_a1;
endmodule


module mantle_wire__typeBitIn4 (
    output [3:0] in,
    input [3:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit4 (
    input [3:0] in,
    output [3:0] out
);
assign out = in;
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

module commonlib_muxn__N2__width4 (
    input [3:0] in_data [1:0],
    input [0:0] in_sel,
    output [3:0] out
);
wire [3:0] _join_out;
coreir_mux #(
    .width(4)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xArray2_Bits2 (
    input [1:0] I0 [1:0],
    input [1:0] I1 [1:0],
    input S,
    output [1:0] O [1:0]
);
wire [3:0] _$_U2_in;
wire [3:0] _$_U3_in;
wire [3:0] _$_U4_out;
wire [3:0] coreir_commonlib_mux2x4_inst0_out;
wire [3:0] _$_U2_out;
assign _$_U2_out = {I0[1][1:0],I0[0][1:0]};
mantle_wire__typeBitIn4 _$_U2 (
    .in(_$_U2_in),
    .out(_$_U2_out)
);
wire [3:0] _$_U3_out;
assign _$_U3_out = {I1[1][1:0],I1[0][1:0]};
mantle_wire__typeBitIn4 _$_U3 (
    .in(_$_U3_in),
    .out(_$_U3_out)
);
mantle_wire__typeBit4 _$_U4 (
    .in(coreir_commonlib_mux2x4_inst0_out),
    .out(_$_U4_out)
);
wire [3:0] coreir_commonlib_mux2x4_inst0_in_data [1:0];
assign coreir_commonlib_mux2x4_inst0_in_data[1] = _$_U3_in;
assign coreir_commonlib_mux2x4_inst0_in_data[0] = _$_U2_in;
wire [0:0] coreir_commonlib_mux2x4_inst0_in_sel;
assign coreir_commonlib_mux2x4_inst0_in_sel[0] = S;
commonlib_muxn__N2__width4 coreir_commonlib_mux2x4_inst0 (
    .in_data(coreir_commonlib_mux2x4_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x4_inst0_in_sel),
    .out(coreir_commonlib_mux2x4_inst0_out)
);
assign O[1] = _$_U4_out[3:2];
assign O[0] = _$_U4_out[1:0];
endmodule

module test_basic_mux_arr (
    input [1:0] I [1:0][1:0],
    input S,
    output [1:0] O [1:0]
);
wire [1:0] Mux2xArray2_Bits2_inst0_O [1:0];
wire [1:0] Mux2xArray2_Bits2_inst0_I0 [1:0];
assign Mux2xArray2_Bits2_inst0_I0[1] = I[0][1];
assign Mux2xArray2_Bits2_inst0_I0[0] = I[0][0];
wire [1:0] Mux2xArray2_Bits2_inst0_I1 [1:0];
assign Mux2xArray2_Bits2_inst0_I1[1] = I[1][1];
assign Mux2xArray2_Bits2_inst0_I1[0] = I[1][0];
Mux2xArray2_Bits2 Mux2xArray2_Bits2_inst0 (
    .I0(Mux2xArray2_Bits2_inst0_I0),
    .I1(Mux2xArray2_Bits2_inst0_I1),
    .S(S),
    .O(Mux2xArray2_Bits2_inst0_O)
);
assign O[1] = Mux2xArray2_Bits2_inst0_O[1];
assign O[0] = Mux2xArray2_Bits2_inst0_O[0];
endmodule


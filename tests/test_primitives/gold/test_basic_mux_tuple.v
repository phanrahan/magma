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

module commonlib_muxn__N2__width3 (
    input [2:0] in_data_0,
    input [2:0] in_data_1,
    input [0:0] in_sel,
    output [2:0] out
);
wire [2:0] _join_out;
coreir_mux #(
    .width(3)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTupleBit_Bits2_Bit (
    input I0__0,
    input [1:0] I0__1,
    input I1__0,
    input [1:0] I1__1,
    output O__0,
    output [1:0] O__1,
    input S
);
wire [2:0] coreir_commonlib_mux2x3_inst0_out;
commonlib_muxn__N2__width3 coreir_commonlib_mux2x3_inst0 (
    .in_data_0({I0__1[1],I0__1[0],I0__0}),
    .in_data_1({I1__1[1],I1__1[0],I1__0}),
    .in_sel(S),
    .out(coreir_commonlib_mux2x3_inst0_out)
);
assign O__0 = coreir_commonlib_mux2x3_inst0_out[0];
assign O__1 = {coreir_commonlib_mux2x3_inst0_out[2],coreir_commonlib_mux2x3_inst0_out[1]};
endmodule

module test_basic_mux_tuple (
    input I_0__0,
    input [1:0] I_0__1,
    input I_1__0,
    input [1:0] I_1__1,
    output O__0,
    output [1:0] O__1,
    input S
);
wire Mux2xTupleBit_Bits2_Bit_inst0_O__0;
wire [1:0] Mux2xTupleBit_Bits2_Bit_inst0_O__1;
Mux2xTupleBit_Bits2_Bit Mux2xTupleBit_Bits2_Bit_inst0 (
    .I0__0(I_0__0),
    .I0__1(I_0__1),
    .I1__0(I_1__0),
    .I1__1(I_1__1),
    .O__0(Mux2xTupleBit_Bits2_Bit_inst0_O__0),
    .O__1(Mux2xTupleBit_Bits2_Bit_inst0_O__1),
    .S(S)
);
assign O__0 = Mux2xTupleBit_Bits2_Bit_inst0_O__0;
assign O__1 = Mux2xTupleBit_Bits2_Bit_inst0_O__1;
endmodule


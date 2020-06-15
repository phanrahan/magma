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

module commonlib_muxn__N2__width6 (
    input [5:0] in_data_0,
    input [5:0] in_data_1,
    input [0:0] in_sel,
    output [5:0] out
);
wire [5:0] _join_out;
coreir_mux #(
    .width(6)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTupleX_Bits2_Y_Bits4 (
    input [1:0] I0_X,
    input [3:0] I0_Y,
    input [1:0] I1_X,
    input [3:0] I1_Y,
    output [1:0] O_X,
    output [3:0] O_Y,
    input S
);
wire [5:0] coreir_commonlib_mux2x6_inst0_out;
commonlib_muxn__N2__width6 coreir_commonlib_mux2x6_inst0 (
    .in_data_0({I0_Y[3],I0_Y[2],I0_Y[1],I0_Y[0],I0_X[1],I0_X[0]}),
    .in_data_1({I1_Y[3],I1_Y[2],I1_Y[1],I1_Y[0],I1_X[1],I1_X[0]}),
    .in_sel(S),
    .out(coreir_commonlib_mux2x6_inst0_out)
);
assign O_X = {coreir_commonlib_mux2x6_inst0_out[1],coreir_commonlib_mux2x6_inst0_out[0]};
assign O_Y = {coreir_commonlib_mux2x6_inst0_out[5],coreir_commonlib_mux2x6_inst0_out[4],coreir_commonlib_mux2x6_inst0_out[3],coreir_commonlib_mux2x6_inst0_out[2]};
endmodule

module test_basic_mux_product (
    input [1:0] I_0_X,
    input [3:0] I_0_Y,
    input [1:0] I_1_X,
    input [3:0] I_1_Y,
    output [1:0] O_X,
    output [3:0] O_Y,
    input S
);
wire [1:0] Mux2xTupleX_Bits2_Y_Bits4_inst0_O_X;
wire [3:0] Mux2xTupleX_Bits2_Y_Bits4_inst0_O_Y;
Mux2xTupleX_Bits2_Y_Bits4 Mux2xTupleX_Bits2_Y_Bits4_inst0 (
    .I0_X(I_0_X),
    .I0_Y(I_0_Y),
    .I1_X(I_1_X),
    .I1_Y(I_1_Y),
    .O_X(Mux2xTupleX_Bits2_Y_Bits4_inst0_O_X),
    .O_Y(Mux2xTupleX_Bits2_Y_Bits4_inst0_O_Y),
    .S(S)
);
assign O_X = Mux2xTupleX_Bits2_Y_Bits4_inst0_O_X;
assign O_Y = Mux2xTupleX_Bits2_Y_Bits4_inst0_O_Y;
endmodule


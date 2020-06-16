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
    input [3:0] in_data_0,
    input [3:0] in_data_1,
    input [0:0] in_sel,
    output [3:0] out
);
wire [3:0] _join_out;
coreir_mux #(
    .width(4)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xArray2_Bits2 (
    input [1:0] I0_0,
    input [1:0] I0_1,
    input [1:0] I1_0,
    input [1:0] I1_1,
    output [1:0] O_0,
    output [1:0] O_1,
    input S
);
wire [3:0] coreir_commonlib_mux2x4_inst0_out;
commonlib_muxn__N2__width4 coreir_commonlib_mux2x4_inst0 (
    .in_data_0({I0_1[1],I0_1[0],I0_0[1],I0_0[0]}),
    .in_data_1({I1_1[1],I1_1[0],I1_0[1],I1_0[0]}),
    .in_sel(S),
    .out(coreir_commonlib_mux2x4_inst0_out)
);
assign O_0 = {coreir_commonlib_mux2x4_inst0_out[1],coreir_commonlib_mux2x4_inst0_out[0]};
assign O_1 = {coreir_commonlib_mux2x4_inst0_out[3],coreir_commonlib_mux2x4_inst0_out[2]};
endmodule

module test_basic_mux_arr (
    input [1:0] I_0_0,
    input [1:0] I_0_1,
    input [1:0] I_1_0,
    input [1:0] I_1_1,
    output [1:0] O_0,
    output [1:0] O_1,
    input S
);
wire [1:0] Mux2xArray2_Bits2_inst0_O_0;
wire [1:0] Mux2xArray2_Bits2_inst0_O_1;
Mux2xArray2_Bits2 Mux2xArray2_Bits2_inst0 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .O_0(Mux2xArray2_Bits2_inst0_O_0),
    .O_1(Mux2xArray2_Bits2_inst0_O_1),
    .S(S)
);
assign O_0 = Mux2xArray2_Bits2_inst0_O_0;
assign O_1 = Mux2xArray2_Bits2_inst0_O_1;
endmodule


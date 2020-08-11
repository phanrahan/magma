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

module commonlib_muxn__N2__width2 (
    input [1:0] in_data [1:0],
    input [0:0] in_sel,
    output [1:0] out
);
wire [1:0] _join_out;
coreir_mux #(
    .width(2)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xBits2 (
    input [1:0] I0,
    input [1:0] I1,
    input S,
    output [1:0] O
);
wire [1:0] coreir_commonlib_mux2x2_inst0_out;
wire [1:0] coreir_commonlib_mux2x2_inst0_in_data [1:0];
assign coreir_commonlib_mux2x2_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x2_inst0_in_data[0] = I0;
commonlib_muxn__N2__width2 coreir_commonlib_mux2x2_inst0 (
    .in_data(coreir_commonlib_mux2x2_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x2_inst0_out)
);
assign O = coreir_commonlib_mux2x2_inst0_out;
endmodule

module test_basic_mux_bits (
    input [1:0] I [1:0],
    input S,
    output [1:0] O
);
wire [1:0] Mux2xBits2_inst0_O;
Mux2xBits2 Mux2xBits2_inst0 (
    .I0(I[0]),
    .I1(I[1]),
    .S(S),
    .O(Mux2xBits2_inst0_O)
);
assign O = Mux2xBits2_inst0_O;
endmodule


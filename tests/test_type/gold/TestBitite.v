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

module commonlib_muxn__N2__width1 (
    input [0:0] in_data [1:0],
    input [0:0] in_sel,
    output [0:0] out
);
wire [0:0] _join_out;
coreir_mux #(
    .width(1)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
wire [0:0] mux_out;
wire [0:0] mux_in_data [1:0];
assign mux_in_data[1] = I1;
assign mux_in_data[0] = I0;
commonlib_muxn__N2__width1 mux (
    .in_data(mux_in_data),
    .in_sel(S),
    .out(mux_out)
);
assign O = mux_out[0];
endmodule

module TestITE (
    input I0,
    input I1,
    input S,
    output O
);
wire Mux2xBit_inst0_O;
Mux2xBit Mux2xBit_inst0 (
    .I0(I1),
    .I1(I0),
    .S(S),
    .O(Mux2xBit_inst0_O)
);
assign O = Mux2xBit_inst0_O;
endmodule


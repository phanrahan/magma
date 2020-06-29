module commonlib_muxn__N2__width1 (
    input [0:0] in_data_0,
    input [0:0] in_data_1,
    input [0:0] in_sel,
    output [0:0] out
);
assign out = in_sel[0] ? in_data_1 : in_data_0;
endmodule

module Mux2xTuplea_OutBit (
    input I0_a,
    input I1_a,
    output O_a,
    input S
);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data_0(I0_a),
    .in_data_1(I1_a),
    .in_sel(S),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O_a = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Test (
    input CLK,
    output O_a,
    input sel
);
Mux2xTuplea_OutBit Mux2xTuplea_OutBit_inst0 (
    .I0_a(1'b1),
    .I1_a(1'b0),
    .O_a(O_a),
    .S(sel)
);
endmodule


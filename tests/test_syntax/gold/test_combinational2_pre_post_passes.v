module commonlib_muxn__N2__width3 (
    input [2:0] in_data_0,
    input [2:0] in_data_1,
    input [0:0] in_sel,
    output [2:0] out
);
assign out = in_sel[0] ? in_data_1 : in_data_0;
endmodule

module Mux2xOutBits3 (
    input [2:0] I0,
    input [2:0] I1,
    input S,
    output [2:0] O
);
commonlib_muxn__N2__width3 coreir_commonlib_mux2x3_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(O)
);
endmodule

module pre_unroll (
    input [2:0] I,
    output [2:0] O
);
wire [2:0] Mux2xOutBits3_inst0_O;
wire [2:0] Mux2xOutBits3_inst1_O;
Mux2xOutBits3 Mux2xOutBits3_inst0 (
    .I0(3'h4),
    .I1(3'h2),
    .S(I[2]),
    .O(Mux2xOutBits3_inst0_O)
);
Mux2xOutBits3 Mux2xOutBits3_inst1 (
    .I0(Mux2xOutBits3_inst0_O),
    .I1(3'h1),
    .S(I[1]),
    .O(Mux2xOutBits3_inst1_O)
);
Mux2xOutBits3 Mux2xOutBits3_inst2 (
    .I0(Mux2xOutBits3_inst1_O),
    .I1(3'h0),
    .S(I[0]),
    .O(O)
);
endmodule


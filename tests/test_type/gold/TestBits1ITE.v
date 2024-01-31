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

module coreir_eq #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 == in1;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module corebit_not (
    input in,
    output out
);
  assign out = ~in;
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

module Mux2xBits1 (
    input [0:0] I0,
    input [0:0] I1,
    input S,
    output [0:0] O
);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
wire [0:0] coreir_commonlib_mux2x1_inst0_in_data [1:0];
assign coreir_commonlib_mux2x1_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x1_inst0_in_data[0] = I0;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data(coreir_commonlib_mux2x1_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out;
endmodule

module TestITE (
    input [0:0] I0,
    input [0:0] I1,
    input [0:0] S,
    output [0:0] O
);
wire [0:0] Mux2xBits1_inst0_O;
wire [0:0] const_0_1_out;
wire magma_Bit_not_inst0_out;
wire magma_Bits_1_eq_inst0_out;
Mux2xBits1 Mux2xBits1_inst0 (
    .I0(I1),
    .I1(I0),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xBits1_inst0_O)
);
coreir_const #(
    .value(1'h0),
    .width(1)
) const_0_1 (
    .out(const_0_1_out)
);
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bits_1_eq_inst0_out),
    .out(magma_Bit_not_inst0_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(S),
    .in1(const_0_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
assign O = Mux2xBits1_inst0_O;
endmodule


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
wire [0:0] _join_in0;
wire [0:0] _join_in1;
wire _join_sel;
wire [0:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(1)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
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
wire [0:0] coreir_commonlib_mux2x1_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x1_inst0_in_sel;
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
assign coreir_commonlib_mux2x1_inst0_in_data = '{I1,I0};
assign coreir_commonlib_mux2x1_inst0_in_sel = S;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data(coreir_commonlib_mux2x1_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x1_inst0_in_sel),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module test_basic_mux (
    input [1:0] I,
    input S,
    output O
);
wire Mux2xBit_inst0_I0;
wire Mux2xBit_inst0_I1;
wire Mux2xBit_inst0_S;
wire Mux2xBit_inst0_O;
assign Mux2xBit_inst0_I0 = I[0];
assign Mux2xBit_inst0_I1 = I[1];
assign Mux2xBit_inst0_S = S;
Mux2xBit Mux2xBit_inst0 (
    .I0(Mux2xBit_inst0_I0),
    .I1(Mux2xBit_inst0_I1),
    .S(Mux2xBit_inst0_S),
    .O(Mux2xBit_inst0_O)
);
assign O = Mux2xBit_inst0_O;
endmodule


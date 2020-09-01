module mantle_wire__typeBitIn6 (
    output [5:0] in,
    input [5:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn4 (
    output [3:0] in,
    input [3:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn2 (
    output [1:0] in,
    input [1:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit6 (
    input [5:0] in,
    output [5:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit4 (
    input [3:0] in,
    output [3:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit2 (
    input [1:0] in,
    output [1:0] out
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

module commonlib_muxn__N2__width6 (
    input [5:0] in_data [1:0],
    input [0:0] in_sel,
    output [5:0] out
);
wire [5:0] _join_out;
coreir_mux #(
    .width(6)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
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
wire [5:0] coreir_commonlib_mux2x6_inst0_out_unq1;
wire [5:0] coreir_commonlib_mux2x6_inst0_in_data_0_in;
wire [5:0] coreir_commonlib_mux2x6_inst0_in_data_1_in;
wire [5:0] coreir_commonlib_mux2x6_inst0_out_out;
wire [1:0] self_I0_X_out;
wire [3:0] self_I0_Y_out;
wire [1:0] self_I1_X_out;
wire [3:0] self_I1_Y_out;
wire [1:0] self_O_X_in;
wire [3:0] self_O_Y_in;
wire [5:0] coreir_commonlib_mux2x6_inst0_in_data [1:0];
assign coreir_commonlib_mux2x6_inst0_in_data[1] = coreir_commonlib_mux2x6_inst0_in_data_1_in;
assign coreir_commonlib_mux2x6_inst0_in_data[0] = coreir_commonlib_mux2x6_inst0_in_data_0_in;
commonlib_muxn__N2__width6 coreir_commonlib_mux2x6_inst0 (
    .in_data(coreir_commonlib_mux2x6_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x6_inst0_out_unq1)
);
wire [5:0] coreir_commonlib_mux2x6_inst0_in_data_0_out;
assign coreir_commonlib_mux2x6_inst0_in_data_0_out = {self_I0_Y_out[3:0],self_I0_X_out[1:0]};
mantle_wire__typeBitIn6 coreir_commonlib_mux2x6_inst0_in_data_0 (
    .in(coreir_commonlib_mux2x6_inst0_in_data_0_in),
    .out(coreir_commonlib_mux2x6_inst0_in_data_0_out)
);
wire [5:0] coreir_commonlib_mux2x6_inst0_in_data_1_out;
assign coreir_commonlib_mux2x6_inst0_in_data_1_out = {self_I1_Y_out[3:0],self_I1_X_out[1:0]};
mantle_wire__typeBitIn6 coreir_commonlib_mux2x6_inst0_in_data_1 (
    .in(coreir_commonlib_mux2x6_inst0_in_data_1_in),
    .out(coreir_commonlib_mux2x6_inst0_in_data_1_out)
);
mantle_wire__typeBit6 coreir_commonlib_mux2x6_inst0_out (
    .in(coreir_commonlib_mux2x6_inst0_out_unq1),
    .out(coreir_commonlib_mux2x6_inst0_out_out)
);
mantle_wire__typeBit2 self_I0_X (
    .in(I0_X),
    .out(self_I0_X_out)
);
mantle_wire__typeBit4 self_I0_Y (
    .in(I0_Y),
    .out(self_I0_Y_out)
);
mantle_wire__typeBit2 self_I1_X (
    .in(I1_X),
    .out(self_I1_X_out)
);
mantle_wire__typeBit4 self_I1_Y (
    .in(I1_Y),
    .out(self_I1_Y_out)
);
mantle_wire__typeBitIn2 self_O_X (
    .in(self_O_X_in),
    .out(coreir_commonlib_mux2x6_inst0_out_out[1:0])
);
mantle_wire__typeBitIn4 self_O_Y (
    .in(self_O_Y_in),
    .out(coreir_commonlib_mux2x6_inst0_out_out[5:2])
);
assign O_X = self_O_X_in;
assign O_Y = self_O_Y_in;
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


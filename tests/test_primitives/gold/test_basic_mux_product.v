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
wire [5:0] _$0_in;
wire [5:0] _$1_in;
wire [5:0] _$2_out;
wire [1:0] _$3_out;
wire [3:0] _$4_out;
wire [1:0] _$5_out;
wire [3:0] _$6_out;
wire [1:0] _$7_in;
wire [3:0] _$8_in;
wire [5:0] coreir_commonlib_mux2x6_inst0_out;
mantle_wire__typeBitIn6 _$0 (
    .in(_$0_in),
    .out({_$4_out[3:0],_$3_out[1:0]})
);
mantle_wire__typeBitIn6 _$1 (
    .in(_$1_in),
    .out({_$6_out[3:0],_$5_out[1:0]})
);
mantle_wire__typeBit6 _$2 (
    .in(coreir_commonlib_mux2x6_inst0_out),
    .out(_$2_out)
);
mantle_wire__typeBit2 _$3 (
    .in(I0_X),
    .out(_$3_out)
);
mantle_wire__typeBit4 _$4 (
    .in(I0_Y),
    .out(_$4_out)
);
mantle_wire__typeBit2 _$5 (
    .in(I1_X),
    .out(_$5_out)
);
mantle_wire__typeBit4 _$6 (
    .in(I1_Y),
    .out(_$6_out)
);
mantle_wire__typeBitIn2 _$7 (
    .in(_$7_in),
    .out(_$2_out[1:0])
);
mantle_wire__typeBitIn4 _$8 (
    .in(_$8_in),
    .out(_$2_out[5:2])
);
commonlib_muxn__N2__width6 coreir_commonlib_mux2x6_inst0 (
    .in_data_0(_$0_in),
    .in_data_1(_$1_in),
    .in_sel(S),
    .out(coreir_commonlib_mux2x6_inst0_out)
);
assign O_X = _$7_in;
assign O_Y = _$8_in;
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


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
wire [3:0] _$0_in;
wire [3:0] _$1_in;
wire [3:0] _$2_out;
wire [1:0] _$3_out;
wire [1:0] _$4_out;
wire [1:0] _$5_out;
wire [1:0] _$6_out;
wire [1:0] _$7_in;
wire [1:0] _$8_in;
wire [3:0] coreir_commonlib_mux2x4_inst0_out;
mantle_wire__typeBitIn4 _$0 (
    .in(_$0_in),
    .out({_$4_out[1:0],_$3_out[1:0]})
);
mantle_wire__typeBitIn4 _$1 (
    .in(_$1_in),
    .out({_$6_out[1:0],_$5_out[1:0]})
);
mantle_wire__typeBit4 _$2 (
    .in(coreir_commonlib_mux2x4_inst0_out),
    .out(_$2_out)
);
mantle_wire__typeBit2 _$3 (
    .in(I0_0),
    .out(_$3_out)
);
mantle_wire__typeBit2 _$4 (
    .in(I0_1),
    .out(_$4_out)
);
mantle_wire__typeBit2 _$5 (
    .in(I1_0),
    .out(_$5_out)
);
mantle_wire__typeBit2 _$6 (
    .in(I1_1),
    .out(_$6_out)
);
mantle_wire__typeBitIn2 _$7 (
    .in(_$7_in),
    .out(_$2_out[1:0])
);
mantle_wire__typeBitIn2 _$8 (
    .in(_$8_in),
    .out(_$2_out[3:2])
);
commonlib_muxn__N2__width4 coreir_commonlib_mux2x4_inst0 (
    .in_data_0(_$0_in),
    .in_data_1(_$1_in),
    .in_sel(S),
    .out(coreir_commonlib_mux2x4_inst0_out)
);
assign O_0 = _$7_in;
assign O_1 = _$8_in;
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


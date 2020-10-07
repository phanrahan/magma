module coreir_sub #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 - in1;
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

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module commonlib_muxn__N2__width8 (
    input [7:0] in_data [1:0],
    input [0:0] in_sel,
    output [7:0] out
);
wire [7:0] _join_out;
coreir_mux #(
    .width(8)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xUInt8 (
    input [7:0] I0,
    input [7:0] I1,
    input S,
    output [7:0] O
);
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
wire [7:0] coreir_commonlib_mux2x8_inst0_in_data [1:0];
assign coreir_commonlib_mux2x8_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x8_inst0_in_data[0] = I0;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data(coreir_commonlib_mux2x8_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Foo_comb (
    input [7:0] val,
    output [7:0] O
);
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_add_inst0_out;
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
coreir_add #(
    .width(8)
) magma_Bits_8_add_inst0 (
    .in0(val),
    .in1(const_1_8_out),
    .out(magma_Bits_8_add_inst0_out)
);
assign O = magma_Bits_8_add_inst0_out;
endmodule

module FooBar_comb (
    input select,
    input [7:0] val,
    input [7:0] self_foo_O,
    input [7:0] self_bar_O,
    output [7:0] O0,
    output [7:0] O1,
    output [7:0] O2
);
wire [7:0] Mux2xUInt8_inst0_O;
wire [7:0] Mux2xUInt8_inst1_O;
wire [7:0] Mux2xUInt8_inst2_O;
Mux2xUInt8 Mux2xUInt8_inst0 (
    .I0(val),
    .I1(val),
    .S(select),
    .O(Mux2xUInt8_inst0_O)
);
Mux2xUInt8 Mux2xUInt8_inst1 (
    .I0(val),
    .I1(val),
    .S(select),
    .O(Mux2xUInt8_inst1_O)
);
Mux2xUInt8 Mux2xUInt8_inst2 (
    .I0(self_bar_O),
    .I1(self_foo_O),
    .S(select),
    .O(Mux2xUInt8_inst2_O)
);
assign O0 = Mux2xUInt8_inst0_O;
assign O1 = Mux2xUInt8_inst1_O;
assign O2 = Mux2xUInt8_inst2_O;
endmodule

module Foo (
    input [7:0] val,
    input CLK,
    output [7:0] O
);
wire [7:0] Foo_comb_inst0_O;
Foo_comb Foo_comb_inst0 (
    .val(val),
    .O(Foo_comb_inst0_O)
);
assign O = Foo_comb_inst0_O;
endmodule

module Bar_comb (
    input [7:0] val,
    output [7:0] O
);
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_sub_inst0_out;
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
coreir_sub #(
    .width(8)
) magma_Bits_8_sub_inst0 (
    .in0(val),
    .in1(const_1_8_out),
    .out(magma_Bits_8_sub_inst0_out)
);
assign O = magma_Bits_8_sub_inst0_out;
endmodule

module Bar (
    input [7:0] val,
    input CLK,
    output [7:0] O
);
wire [7:0] Bar_comb_inst0_O;
Bar_comb Bar_comb_inst0 (
    .val(val),
    .O(Bar_comb_inst0_O)
);
assign O = Bar_comb_inst0_O;
endmodule

module FooBar (
    input select,
    input [7:0] val,
    input CLK,
    output [7:0] O
);
wire [7:0] Bar_inst0_O;
wire [7:0] FooBar_comb_inst0_O0;
wire [7:0] FooBar_comb_inst0_O1;
wire [7:0] FooBar_comb_inst0_O2;
wire [7:0] Foo_inst0_O;
Bar Bar_inst0 (
    .val(FooBar_comb_inst0_O1),
    .CLK(CLK),
    .O(Bar_inst0_O)
);
FooBar_comb FooBar_comb_inst0 (
    .select(select),
    .val(val),
    .self_foo_O(Foo_inst0_O),
    .self_bar_O(Bar_inst0_O),
    .O0(FooBar_comb_inst0_O0),
    .O1(FooBar_comb_inst0_O1),
    .O2(FooBar_comb_inst0_O2)
);
Foo Foo_inst0 (
    .val(FooBar_comb_inst0_O0),
    .CLK(CLK),
    .O(Foo_inst0_O)
);
assign O = FooBar_comb_inst0_O2;
endmodule


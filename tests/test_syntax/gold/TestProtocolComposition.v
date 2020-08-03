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
wire [7:0] _join_in0;
wire [7:0] _join_in1;
wire _join_sel;
wire [7:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(8)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutUInt8 (
    input [7:0] I0,
    input [7:0] I1,
    input S,
    output [7:0] O
);
wire [7:0] coreir_commonlib_mux2x8_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x8_inst0_in_sel;
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
assign coreir_commonlib_mux2x8_inst0_in_data = '{I1,I0};
assign coreir_commonlib_mux2x8_inst0_in_sel = S;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data(coreir_commonlib_mux2x8_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x8_inst0_in_sel),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Foo_comb (
    input [7:0] val,
    output [7:0] O
);
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_add_inst0_in0;
wire [7:0] magma_Bits_8_add_inst0_in1;
wire [7:0] magma_Bits_8_add_inst0_out;
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
assign magma_Bits_8_add_inst0_in0 = val;
assign magma_Bits_8_add_inst0_in1 = const_1_8_out;
coreir_add #(
    .width(8)
) magma_Bits_8_add_inst0 (
    .in0(magma_Bits_8_add_inst0_in0),
    .in1(magma_Bits_8_add_inst0_in1),
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
wire [7:0] Mux2xOutUInt8_inst0_I0;
wire [7:0] Mux2xOutUInt8_inst0_I1;
wire Mux2xOutUInt8_inst0_S;
wire [7:0] Mux2xOutUInt8_inst0_O;
wire [7:0] Mux2xOutUInt8_inst1_I0;
wire [7:0] Mux2xOutUInt8_inst1_I1;
wire Mux2xOutUInt8_inst1_S;
wire [7:0] Mux2xOutUInt8_inst1_O;
wire [7:0] Mux2xOutUInt8_inst2_I0;
wire [7:0] Mux2xOutUInt8_inst2_I1;
wire Mux2xOutUInt8_inst2_S;
wire [7:0] Mux2xOutUInt8_inst2_O;
assign Mux2xOutUInt8_inst0_I0 = val;
assign Mux2xOutUInt8_inst0_I1 = val;
assign Mux2xOutUInt8_inst0_S = select;
Mux2xOutUInt8 Mux2xOutUInt8_inst0 (
    .I0(Mux2xOutUInt8_inst0_I0),
    .I1(Mux2xOutUInt8_inst0_I1),
    .S(Mux2xOutUInt8_inst0_S),
    .O(Mux2xOutUInt8_inst0_O)
);
assign Mux2xOutUInt8_inst1_I0 = val;
assign Mux2xOutUInt8_inst1_I1 = val;
assign Mux2xOutUInt8_inst1_S = select;
Mux2xOutUInt8 Mux2xOutUInt8_inst1 (
    .I0(Mux2xOutUInt8_inst1_I0),
    .I1(Mux2xOutUInt8_inst1_I1),
    .S(Mux2xOutUInt8_inst1_S),
    .O(Mux2xOutUInt8_inst1_O)
);
assign Mux2xOutUInt8_inst2_I0 = self_bar_O;
assign Mux2xOutUInt8_inst2_I1 = self_foo_O;
assign Mux2xOutUInt8_inst2_S = select;
Mux2xOutUInt8 Mux2xOutUInt8_inst2 (
    .I0(Mux2xOutUInt8_inst2_I0),
    .I1(Mux2xOutUInt8_inst2_I1),
    .S(Mux2xOutUInt8_inst2_S),
    .O(Mux2xOutUInt8_inst2_O)
);
assign O0 = Mux2xOutUInt8_inst0_O;
assign O1 = Mux2xOutUInt8_inst1_O;
assign O2 = Mux2xOutUInt8_inst2_O;
endmodule

module Foo (
    input [7:0] val,
    input CLK,
    output [7:0] O
);
wire [7:0] Foo_comb_inst0_val;
wire [7:0] Foo_comb_inst0_O;
assign Foo_comb_inst0_val = val;
Foo_comb Foo_comb_inst0 (
    .val(Foo_comb_inst0_val),
    .O(Foo_comb_inst0_O)
);
assign O = Foo_comb_inst0_O;
endmodule

module Bar_comb (
    input [7:0] val,
    output [7:0] O
);
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_sub_inst0_in0;
wire [7:0] magma_Bits_8_sub_inst0_in1;
wire [7:0] magma_Bits_8_sub_inst0_out;
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
assign magma_Bits_8_sub_inst0_in0 = val;
assign magma_Bits_8_sub_inst0_in1 = const_1_8_out;
coreir_sub #(
    .width(8)
) magma_Bits_8_sub_inst0 (
    .in0(magma_Bits_8_sub_inst0_in0),
    .in1(magma_Bits_8_sub_inst0_in1),
    .out(magma_Bits_8_sub_inst0_out)
);
assign O = magma_Bits_8_sub_inst0_out;
endmodule

module Bar (
    input [7:0] val,
    input CLK,
    output [7:0] O
);
wire [7:0] Bar_comb_inst0_val;
wire [7:0] Bar_comb_inst0_O;
assign Bar_comb_inst0_val = val;
Bar_comb Bar_comb_inst0 (
    .val(Bar_comb_inst0_val),
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
wire [7:0] Bar_inst0_val;
wire Bar_inst0_CLK;
wire [7:0] Bar_inst0_O;
wire FooBar_comb_inst0_select;
wire [7:0] FooBar_comb_inst0_val;
wire [7:0] FooBar_comb_inst0_self_foo_O;
wire [7:0] FooBar_comb_inst0_self_bar_O;
wire [7:0] FooBar_comb_inst0_O0;
wire [7:0] FooBar_comb_inst0_O1;
wire [7:0] FooBar_comb_inst0_O2;
wire [7:0] Foo_inst0_val;
wire Foo_inst0_CLK;
wire [7:0] Foo_inst0_O;
assign Bar_inst0_val = FooBar_comb_inst0_O1;
assign Bar_inst0_CLK = CLK;
Bar Bar_inst0 (
    .val(Bar_inst0_val),
    .CLK(Bar_inst0_CLK),
    .O(Bar_inst0_O)
);
assign FooBar_comb_inst0_select = select;
assign FooBar_comb_inst0_val = val;
assign FooBar_comb_inst0_self_foo_O = Foo_inst0_O;
assign FooBar_comb_inst0_self_bar_O = Bar_inst0_O;
FooBar_comb FooBar_comb_inst0 (
    .select(FooBar_comb_inst0_select),
    .val(FooBar_comb_inst0_val),
    .self_foo_O(FooBar_comb_inst0_self_foo_O),
    .self_bar_O(FooBar_comb_inst0_self_bar_O),
    .O0(FooBar_comb_inst0_O0),
    .O1(FooBar_comb_inst0_O1),
    .O2(FooBar_comb_inst0_O2)
);
assign Foo_inst0_val = FooBar_comb_inst0_O0;
assign Foo_inst0_CLK = CLK;
Foo Foo_inst0 (
    .val(Foo_inst0_val),
    .CLK(Foo_inst0_CLK),
    .O(Foo_inst0_O)
);
assign O = FooBar_comb_inst0_O2;
endmodule


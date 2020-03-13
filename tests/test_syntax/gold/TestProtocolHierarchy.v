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
    input [7:0] self_f_O,
    output [7:0] O0,
    output [7:0] O1
);
assign O0 = val;
assign O1 = self_f_O;
endmodule

module Bar (
    input [7:0] val,
    input CLK,
    output [7:0] O
);
wire [7:0] Bar_comb_inst0_O0;
wire [7:0] Bar_comb_inst0_O1;
wire [7:0] Foo_inst0_O;
Bar_comb Bar_comb_inst0 (
    .val(val),
    .self_f_O(Foo_inst0_O),
    .O0(Bar_comb_inst0_O0),
    .O1(Bar_comb_inst0_O1)
);
Foo Foo_inst0 (
    .val(Bar_comb_inst0_O0),
    .CLK(CLK),
    .O(Foo_inst0_O)
);
assign O = Bar_comb_inst0_O1;
endmodule


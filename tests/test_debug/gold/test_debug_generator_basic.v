module coreir_xorr #(
    parameter width = 1
) (
    input [width-1:0] in,
    output out
);
  assign out = ^in;
endmodule

module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
endmodule

module coreir_not #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = ~in;
endmodule

module Foo (
    input [3:0] I,
    output O
);
wire coreir_xorr_4_inst0_out;
wire [3:0] magma_Bits_4_not_inst0_out;
wire [3:0] x_out;
coreir_xorr #(
    .width(4)
) coreir_xorr_4_inst0 (
    .in(x_out),
    .out(coreir_xorr_4_inst0_out)
);
coreir_not #(
    .width(4)
) magma_Bits_4_not_inst0 (
    .in(I),
    .out(magma_Bits_4_not_inst0_out)
);
coreir_wire #(
    .width(4)
) x (
    .in(magma_Bits_4_not_inst0_out),
    .out(x_out)
);
assign O = coreir_xorr_4_inst0_out;
endmodule


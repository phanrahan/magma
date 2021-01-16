module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module Foo (
    input [31:0] bus_in_addr,
    input [31:0] bus_in_data,
    output [31:0] data_out
);
wire [31:0] const_0_32_out;
coreir_const #(
    .value(32'h00000000),
    .width(32)
) const_0_32 (
    .out(const_0_32_out)
);
assign data_out = const_0_32_out;
endmodule


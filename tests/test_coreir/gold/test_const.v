module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module Main (
    output [2:0] O_0
);
wire [2:0] const_0_3_out;
coreir_const #(
    .value(3'h0),
    .width(3)
) const_0_3 (
    .out(const_0_3_out)
);
assign O_0 = const_0_3_out;
endmodule


module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module enum_test (
    input [1:0] I,
    output [1:0] O [1:0]
);
wire [1:0] const_0_2_out;
coreir_const #(
    .value(2'h0),
    .width(2)
) const_0_2 (
    .out(const_0_2_out)
);
assign O[1] = const_0_2_out;
assign O[0] = I;
endmodule


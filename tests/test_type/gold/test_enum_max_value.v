module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module enum_test_max_value (
    input [2:0] I,
    output [2:0] O [1:0]
);
wire [2:0] const_4_3_out;
coreir_const #(
    .value(3'h4),
    .width(3)
) const_4_3 (
    .out(const_4_3_out)
);
assign O[1] = const_4_3_out;
assign O[0] = I;
endmodule


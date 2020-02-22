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
    output [2:0] O_0,
    output [2:0] O_1
);
wire [2:0] const_4_3_out;
coreir_const #(
    .value(3'h4),
    .width(3)
) const_4_3 (
    .out(const_4_3_out)
);
assign O_0 = I;
assign O_1 = const_4_3_out;
endmodule


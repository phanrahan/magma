module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

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
wire [1:0] Const_inst0_out;
coreir_const #(
    .value(2'h0),
    .width(2)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_term #(
    .width(2)
) term_inst0 (
    .in(Const_inst0_out)
);
assign O[1] = Const_inst0_out;
assign O[0] = I;
endmodule


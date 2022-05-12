// Module `InlineVerilogExpression_a489b4461c0192fc` defined externally
module corebit_term (
    input in
);

endmodule

module RegWrapper (
    input I,
    output O,
    input CLK
);
wire _magma_inline_wire0;
InlineVerilogExpression_a489b4461c0192fc InlineVerilogExpression_a489b4461c0192fc_inst0 (
    .O(O)
);
assign _magma_inline_wire0 = I;
reg [0:0] R;
asssign R <= _magma_inline_wire0;

endmodule


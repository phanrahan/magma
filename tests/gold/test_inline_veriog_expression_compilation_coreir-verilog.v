// Module `InlineVerilogExpression_Bits2_a489b4461c0192fc` defined externally
// Module `InlineVerilogExpression_Bits1_a489b4461c0192fc` defined externally
module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module MyWrapperGen_2 (
    input [1:0] I,
    output [1:0] O,
    input CLK
);
wire [1:0] _magma_inline_wire0;
InlineVerilogExpression_Bits2_a489b4461c0192fc InlineVerilogExpression_Bits2_a489b4461c0192fc_inst0 (
    .O(O)
);
assign _magma_inline_wire0 = I;
reg [1:0] R;
asssign R <= _magma_inline_wire0;

endmodule

module MyWrapperGen_1 (
    input [0:0] I,
    output [0:0] O,
    input CLK
);
wire [0:0] _magma_inline_wire0;
InlineVerilogExpression_Bits1_a489b4461c0192fc InlineVerilogExpression_Bits1_a489b4461c0192fc_inst0 (
    .O(O)
);
assign _magma_inline_wire0 = I;
reg [0:0] R;
asssign R <= _magma_inline_wire0;

endmodule

module Top (
    input [1:0] I,
    output [1:0] O,
    input CLK
);
wire [0:0] MyWrapperGen_1_inst0_O;
MyWrapperGen_1 MyWrapperGen_1_inst0 (
    .I(I[0]),
    .O(MyWrapperGen_1_inst0_O),
    .CLK(CLK)
);
wire [1:0] MyWrapperGen_2_inst0_I;
assign MyWrapperGen_2_inst0_I = {MyWrapperGen_1_inst0_O[0],MyWrapperGen_1_inst0_O[0]};
MyWrapperGen_2 MyWrapperGen_2_inst0 (
    .I(MyWrapperGen_2_inst0_I),
    .O(O),
    .CLK(CLK)
);
endmodule


module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module corebit_term (
    input in
);

endmodule

module Bottom (
    input I,
    output O
);
assign O = I;
endmodule

module Middle (
    input I,
    output O
);
wire _magma_bind_wire_0_out;
wire bottom_O;
corebit_wire _magma_bind_wire_0 (
    .in(I),
    .out(_magma_bind_wire_0_out)
);
Bottom bottom (
    .I(I),
    .O(bottom_O)
);
corebit_term corebit_term_inst0 (
    .in(_magma_bind_wire_0_out)
);
assign O = bottom_O;
endmodule

module Top (
    input I,
    output O
);
wire middle_O;
Middle middle (
    .I(I),
    .O(middle_O)
);
assign O = middle_O;
endmodule


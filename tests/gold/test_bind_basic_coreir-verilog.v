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

module Top (
    input I,
    output O
);
wire _magma_bind_wire_0_out;
corebit_wire _magma_bind_wire_0 (
    .in(I),
    .out(_magma_bind_wire_0_out)
);
corebit_term corebit_term_inst0 (
    .in(_magma_bind_wire_0_out)
);
assign O = I;
endmodule


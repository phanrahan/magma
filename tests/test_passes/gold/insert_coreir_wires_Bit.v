module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module Main (
    input I,
    output O
);
wire x_out;
corebit_wire x (
    .in(I),
    .out(x_out)
);
assign O = x_out;
endmodule


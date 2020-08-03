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
wire x_in;
wire x_out;
assign x_in = I;
corebit_wire x (
    .in(x_in),
    .out(x_out)
);
assign O = x_out;
endmodule


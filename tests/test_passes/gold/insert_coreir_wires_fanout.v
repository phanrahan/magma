module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module Main (
    input I,
    output O0,
    output O1
);
wire x_out;
corebit_wire x (
    .in(I),
    .out(x_out)
);
assign O0 = x_out;
assign O1 = x_out;
endmodule


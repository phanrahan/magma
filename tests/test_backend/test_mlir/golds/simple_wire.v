module simple_wire(
  input  [7:0] I,
  output [7:0] O
);

  wire [7:0] tmp = I;
  assign O = tmp;
endmodule


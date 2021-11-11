module simple_wire(
  input  [7:0] I,
  output [7:0] O);

  wire [7:0] tmp;	// <stdin>:3:12

  assign tmp = I;	// <stdin>:4:5
  assign O = tmp;	// <stdin>:5:10, :6:5
endmodule


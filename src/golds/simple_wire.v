module simple_wire(	// <stdin>:1:1
  input  [7:0] I,
  output [7:0] O);

  wire [7:0] tmp;	// <stdin>:2:10

  assign tmp = I;	// <stdin>:3:5
  assign O = tmp;	// <stdin>:4:10, :5:5
endmodule


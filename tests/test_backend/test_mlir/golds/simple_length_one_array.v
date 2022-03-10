module simple_length_one_array(	// <stdin>:1:1
  input  [0:0][7:0] I,
  output [7:0]      O);

wire [1:0][7:0] _T = {{{8'h0}}, I};	// <stdin>:2:10, :3:10, :4:10
  assign O = _T[1'h0];	// <stdin>:5:10, :6:10, :7:5
endmodule


module simple_length_one_array(
  input  [0:0][7:0] I,
  output [7:0]      O);

  assign O = ({I, {{8'h0}}})[1'h0];	// <stdin>:3:14, :4:14, :5:10, :6:10, :7:10, :8:5
endmodule


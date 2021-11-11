module simple_mux_wrapper(
  input  [7:0] a,
  input        s,
  output [7:0] y);

  assign y = ({{a}, {~a}})[s];	// <stdin>:4:10, :5:10, :6:10, :7:5
endmodule


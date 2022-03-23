module simple_aggregates_array(	// <stdin>:1:1
  input  [7:0][15:0] a,
  output [7:0][15:0] y,
  output [3:0][15:0] z);

  assign y = {{a[3'h3]}, {a[3'h2]}, {a[3'h1]}, {a[3'h0]}, {a[3'h7]}, {a[3'h6]}, {a[3'h5]}, {a[3'h4]}};	// <stdin>:2:10, :3:10, :4:10, :5:10, :6:10, :7:10, :8:10, :9:10, :10:10, :11:10, :12:11, :13:11, :14:11, :15:11, :16:11, :17:11, :18:11, :20:5
  assign z = a[3'h0 +: 4];	// <stdin>:10:10, :19:11, :20:5
endmodule


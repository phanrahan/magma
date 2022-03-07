module VecSearch(	// <stdin>:1:1
  input        CLK,
  output [3:0] out);

  reg [2:0] Register_inst0;	// <stdin>:11:11

  always_ff @(posedge CLK)	// <stdin>:12:5
    Register_inst0 <= Register_inst0 + 3'h1;	// <stdin>:9:10, :10:10, :13:9, :19:10
  initial	// <stdin>:16:5
    Register_inst0 = 3'h0;	// <stdin>:15:11, :17:9
  wire [6:0][3:0] _T = {{4'h0}, {4'h4}, {4'hF}, {4'hE}, {4'h2}, {4'h5}, {4'hD}};	// <stdin>:2:10, :3:10, :4:10, :5:10, :6:10, :7:10, :8:10, :20:11
  assign out = _T[Register_inst0];	// <stdin>:19:10, :21:11, :22:5
endmodule


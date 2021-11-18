module Parity(	// <stdin>:1:1
  input  I, CLK,
  output O);

  reg Register_inst0;	// <stdin>:12:11

  always_ff @(posedge CLK) begin	// <stdin>:13:5
    automatic logic [1:0] _T = {{1'h0}, {1'h1}};	// <stdin>:2:10, :3:10, :8:10
    automatic logic [1:0] _T_0 = {{Register_inst0}, {_T[~Register_inst0]}};	// <stdin>:7:10, :9:10, :10:11, :20:10

    Register_inst0 <= _T_0[I];	// <stdin>:11:10, :14:9
  end // always_ff @(posedge)
  initial	// <stdin>:17:5
    Register_inst0 = 1'h0;	// <stdin>:2:10, :18:9
  assign O = Register_inst0;	// <stdin>:20:10, :24:5
endmodule


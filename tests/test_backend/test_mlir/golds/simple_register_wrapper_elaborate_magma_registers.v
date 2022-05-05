module Register(	// <stdin>:1:1
  input  [7:0] I,
  input        CLK,
  output [7:0] O);

  reg [7:0] reg_P8_inst0;	// <stdin>:2:10

  always_ff @(posedge CLK)	// <stdin>:3:5
    reg_P8_inst0 <= I;	// <stdin>:4:9
  initial	// <stdin>:7:5
    reg_P8_inst0 = 8'h3;	// <stdin>:6:10, :8:9
  assign O = reg_P8_inst0;	// <stdin>:10:10, :11:5
endmodule

module simple_register_wrapper(	// <stdin>:13:1
  input  [7:0] a,
  input        CLK,
  output [7:0] y);

  Register reg0 (	// <stdin>:14:10
    .I   (a),
    .CLK (CLK),
    .O   (y)
  );
endmodule


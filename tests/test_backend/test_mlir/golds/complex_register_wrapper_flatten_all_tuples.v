module complex_register_wrapper(	// <stdin>:1:1
  input  [7:0]       a_x,
  input              a_y,
  input  [5:0][15:0] b,
  input              CLK, CE, ASYNCRESET,
  output [7:0]       y_u_x,
  output             y_u_y,
  output [5:0][15:0] y_v);

  reg [7:0]       Register_inst0;	// <stdin>:2:10
  reg             Register_inst0_0;	// <stdin>:15:10
  reg [5:0][15:0] Register_inst1;	// <stdin>:28:10
  reg [7:0]       Register_inst2;	// <stdin>:43:11

  always_ff @(posedge CLK or posedge ASYNCRESET) begin	// <stdin>:16:5
    if (ASYNCRESET) begin	// <stdin>:16:5
      Register_inst0 <= 8'hA;	// <stdin>:8:9, :10:10
      Register_inst0_0 <= 1'h1;	// <stdin>:21:9, :23:10
    end
    else begin	// <stdin>:16:5
      if (CE)	// <stdin>:4:9
        Register_inst0 <= a_x;	// <stdin>:5:13
      if (CE)	// <stdin>:17:9
        Register_inst0_0 <= a_y;	// <stdin>:18:13
    end
  end // always_ff @(posedge or posedge)
  always_ff @(posedge CLK) begin	// <stdin>:44:5
    Register_inst1 <= b;	// <stdin>:30:9
    if (CE)	// <stdin>:45:9
      Register_inst2 <= a_x;	// <stdin>:46:13
  end // always_ff @(posedge)
  initial begin	// <stdin>:50:5
    Register_inst0 = 8'hA;	// <stdin>:10:10, :12:9
    Register_inst0_0 = 1'h1;	// <stdin>:23:10, :25:9
    Register_inst1 = {{16'h0}, {16'h2}, {16'h4}, {16'h6}, {16'h8}, {16'hA}};	// <stdin>:32:10, :33:11, :34:11, :35:11, :36:11, :37:11, :38:10, :40:9
    Register_inst2 = 8'h0;	// <stdin>:49:11, :51:9
  end // initial
  assign y_u_x = Register_inst0;	// <stdin>:14:10, :54:5
  assign y_u_y = Register_inst0_0;	// <stdin>:27:10, :54:5
  assign y_v = Register_inst1;	// <stdin>:42:10, :54:5
endmodule


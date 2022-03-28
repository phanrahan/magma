module complex_compile_guard2(	// <stdin>:1:1
  input  [7:0] I_x,
  input        O_y, CLK,
  output       I_y,
  output [7:0] O_x);

  `ifdef COND1	// <stdin>:11:5
    reg [7:0] Register_inst0;	// <stdin>:12:15
    reg       Register_inst1;	// <stdin>:21:15

    always_ff @(posedge CLK) begin	// <stdin>:22:9
      Register_inst0 <= {I_x[3:0], I_x[7:4]};	// <stdin>:10:10, :14:13
      Register_inst1 <= Register_inst0[0];	// <stdin>:19:14, :20:15, :23:13
    end // always_ff @(posedge)
    initial begin	// <stdin>:25:9
      Register_inst0 = 8'h0;	// <stdin>:17:13, :30:11
      Register_inst1 = 1'h0;	// <stdin>:26:13, :31:11
    end // initial
  `endif
  assign I_y = O_y;	// <stdin>:32:5
  assign O_x = I_x;	// <stdin>:32:5
endmodule


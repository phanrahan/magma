module complex_compile_guard2(	// <stdin>:1:1
  input  [7:0] I_x,
  input        O_y, CLK,
  output       I_y,
  output [7:0] O_x);

  `ifdef COND1	// <stdin>:11:5
    reg [7:0] Register_inst0;	// <stdin>:12:15
    reg       Register_inst3;	// <stdin>:51:15

    `ifndef COND2	// <stdin>:23:9
      reg [1:0] Register_inst1;	// <stdin>:25:19

      always_ff @(posedge CLK)	// <stdin>:26:13
        Register_inst1 <= Register_inst0[6:5];	// <stdin>:19:14, :22:15, :27:17
      initial	// <stdin>:29:13
        Register_inst1 = 2'h0;	// <stdin>:30:17, :61:11
    `endif
    `ifndef COND3	// <stdin>:39:9
      reg [5:0] Register_inst2;	// <stdin>:41:19

      always_ff @(posedge CLK)	// <stdin>:42:13
        Register_inst2 <= Register_inst0[7:2];	// <stdin>:19:14, :38:15, :43:17
      initial	// <stdin>:45:13
        Register_inst2 = 6'h0;	// <stdin>:46:17, :62:11
    `endif
    always_ff @(posedge CLK) begin	// <stdin>:52:9
      Register_inst0 <= {I_x[3:0], I_x[7:4]};	// <stdin>:10:10, :14:13
      Register_inst3 <= Register_inst0[0];	// <stdin>:19:14, :50:15, :53:13
    end // always_ff @(posedge)
    initial begin	// <stdin>:55:9
      Register_inst0 = 8'h0;	// <stdin>:17:13, :60:11
      Register_inst3 = 1'h0;	// <stdin>:56:13, :63:11
    end // initial
  `endif
  assign I_y = O_y;	// <stdin>:64:5
  assign O_x = I_x;	// <stdin>:64:5
endmodule


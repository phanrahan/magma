module complex_compile_guard2(	// <stdin>:1:1
  input  struct packed {logic [3:0] a; logic [3:0] b; } I_x,
  input                                                 O_y, CLK,
  output                                                I_y,
  output struct packed {logic [3:0] a; logic [3:0] b; } O_x);

  `ifdef COND1	// <stdin>:5:5
    struct packed {logic [3:0] a; logic [3:0] b; } Register_inst0;	// <stdin>:6:14

    wire struct packed {logic [3:0] a; logic [3:0] b; } _T = '{a: (4'h0), b: (4'h0)};	// <stdin>:41:10, :43:10
    always_ff @(posedge CLK) begin	// <stdin>:7:9
      automatic struct packed {logic [3:0] a; logic [3:0] b; } _T_1 = '{a: I_x.b, b: I_x.a};	// <stdin>:2:10, :3:10, :4:10

      Register_inst0 <= _T_1;	// <stdin>:8:13
    end // always_ff @(posedge)
    initial	// <stdin>:10:9
      Register_inst0 = _T;	// <stdin>:11:13
    wire [3:0] _T_0 = Register_inst0.a;	// <stdin>:13:14, :15:14
    `ifdef COND2	// <stdin>:17:9
      struct packed {logic [3:0] a; logic [3:0] b; } Register_inst1;	// <stdin>:18:19

      always_ff @(posedge CLK) begin	// <stdin>:19:13
        automatic struct packed {logic [3:0] a; logic [3:0] b; } _T_2 = '{a: Register_inst0.b, b: _T_0};	// <stdin>:13:14, :14:14, :16:15

        Register_inst1 <= _T_2;	// <stdin>:20:17
      end // always_ff @(posedge)
      initial	// <stdin>:22:13
        Register_inst1 = _T;	// <stdin>:23:17
    `endif
    `ifdef COND3	// <stdin>:30:9
      reg [1:0] Register_inst2;	// <stdin>:31:19

      always_ff @(posedge CLK)	// <stdin>:32:13
        Register_inst2 <= _T_0[2:1];	// <stdin>:29:15, :33:17
      initial	// <stdin>:35:13
        Register_inst2 = 2'h0;	// <stdin>:36:17, :44:11
    `endif
  `endif
  assign I_y = O_y;	// <stdin>:45:5
  assign O_x = I_x;	// <stdin>:45:5
endmodule


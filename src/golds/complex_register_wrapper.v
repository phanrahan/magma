module complex_register_wrapper(
  input  struct packed {logic [7:0] x; logic y; }                                          a,
  input  [5:0][15:0]                                                                       b,
  input                                                                                    CLK,
  input                                                                                    ASYNCRESET,
  output struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } y);

  wire struct packed {logic [7:0] x; logic y; } _T;	// <stdin>:17:10
      struct packed {logic [7:0] x; logic y; } Register_inst0;	// <stdin>:11:23
  reg  [5:0][15:0]                              Register_inst1;	// <stdin>:19:23

  always @(posedge CLK or posedge ASYNCRESET) begin	// <stdin>:12:5
    if (ASYNCRESET)	// <stdin>:12:5
      Register_inst0 <= _T;	// <stdin>:15:7, :17:10
    else	// <stdin>:12:5
      Register_inst0 <= a;	// <stdin>:13:7
  end // always @(posedge or posedge)
  wire struct packed {logic [7:0] x; logic y; } _T_0 = '{x: (8'hA), y: (1'h1)};	// <stdin>:9:13, :10:15, :17:10
  assign _T = _T_0;	// <stdin>:17:10
  always @(posedge CLK)	// <stdin>:20:5
    Register_inst1 <= b;	// <stdin>:21:7
  wire [5:0][15:0] _T_1 = {{16'h0}, {16'h2}, {16'h4}, {16'h6}, {16'h8}, {16'hA}};	// <stdin>:3:16, :4:15, :5:15, :6:15, :7:15, :8:15, :23:10
  initial begin	// <stdin>:24:5
    Register_inst0 = _T;	// <stdin>:17:10, :25:7
    Register_inst1 = _T_1;	// <stdin>:26:7
  end // initial
  wire struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } _T_2 = '{u: Register_inst0, v: Register_inst1};	// <stdin>:18:10, :28:10, :29:10
  assign y = _T_2;	// <stdin>:30:5
endmodule


module complex_register_wrapper(	// <stdin>:1:1
  input  struct packed {logic [7:0] x; logic y; }                                          a,
  input  [5:0][15:0]                                                                       b,
  input                                                                                    CLK,
  input                                                                                    ASYNCRESET,
  output struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } y);

  wire struct packed {logic [7:0] x; logic y; } _T;	// <stdin>:10:10
      struct packed {logic [7:0] x; logic y; } Register_inst0;	// <stdin>:2:10
  reg  [5:0][15:0]                              Register_inst1;	// <stdin>:15:10

  always_ff @(posedge CLK or posedge ASYNCRESET) begin	// <stdin>:3:5
    if (ASYNCRESET)	// <stdin>:3:5
      Register_inst0 <= _T;	// <stdin>:6:9, :10:10
    else	// <stdin>:3:5
      Register_inst0 <= a;	// <stdin>:4:9
  end // always_ff @(posedge or posedge)
  wire struct packed {logic [7:0] x; logic y; } _T_0 = '{x: (8'hA), y: (1'h1)};	// <stdin>:8:10, :9:10, :10:10
  assign _T = _T_0;	// <stdin>:10:10
  always_ff @(posedge CLK)	// <stdin>:16:5
    Register_inst1 <= b;	// <stdin>:17:9
  initial begin	// <stdin>:26:5
    Register_inst0 = _T;	// <stdin>:10:10, :12:9
    Register_inst1 = {{16'h0}, {16'h2}, {16'h4}, {16'h6}, {16'h8}, {16'hA}};	// <stdin>:19:10, :20:10, :21:11, :22:11, :23:11, :24:11, :25:10, :27:9
  end // initial
  assign y = '{u: Register_inst0, v: Register_inst1};	// <stdin>:14:10, :29:10, :30:11, :31:5
endmodule


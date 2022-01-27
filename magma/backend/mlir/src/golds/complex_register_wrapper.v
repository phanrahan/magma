module complex_register_wrapper(	// <stdin>:1:1
  input  struct packed {logic [7:0] x; logic y; }                                          a,
  input  [5:0][15:0]                                                                       b,
  input                                                                                    CLK,
  input                                                                                    CE,
  input                                                                                    ASYNCRESET,
  output struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } y);

  wire struct packed {logic [7:0] x; logic y; } _T;	// <stdin>:12:10
      struct packed {logic [7:0] x; logic y; } Register_inst0;	// <stdin>:2:10
  reg  [5:0][15:0]                              Register_inst1;	// <stdin>:17:10
  reg  [7:0]                                    Register_inst2;	// <stdin>:34:11

  always_ff @(posedge CLK or posedge ASYNCRESET) begin	// <stdin>:3:5
    if (ASYNCRESET)	// <stdin>:3:5
      Register_inst0 <= _T;	// <stdin>:8:9, :12:10
    else begin	// <stdin>:3:5
      if (CE)	// <stdin>:4:9
        Register_inst0 <= a;	// <stdin>:5:13
    end
  end // always_ff @(posedge or posedge)
  wire struct packed {logic [7:0] x; logic y; } _T_0 = '{x: (8'hA), y: (1'h1)};	// <stdin>:10:10, :11:10, :12:10
  assign _T = _T_0;	// <stdin>:12:10
  always_ff @(posedge CLK) begin	// <stdin>:35:5
    Register_inst1 <= b;	// <stdin>:19:9
    if (CE)	// <stdin>:36:9
      Register_inst2 <= a.x;	// <stdin>:33:11, :37:13
  end // always_ff @(posedge)
  initial begin	// <stdin>:41:5
    Register_inst0 = _T;	// <stdin>:12:10, :14:9
    Register_inst1 = {{16'h0}, {16'h2}, {16'h4}, {16'h6}, {16'h8}, {16'hA}};	// <stdin>:21:10, :22:10, :23:11, :24:11, :25:11, :26:11, :27:10, :29:9
    Register_inst2 = 8'h0;	// <stdin>:40:11, :42:9
  end // initial
  assign y = '{u: Register_inst0, v: Register_inst1};	// <stdin>:16:10, :31:10, :32:11, :45:5
endmodule


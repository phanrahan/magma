module complex_register_wrapper(	// <stdin>:1:1
  input  struct packed {logic [7:0] x; logic y; }                                          a,
  input  [5:0][15:0]                                                                       b,
  input                                                                                    CLK,
  input                                                                                    CE,
  input                                                                                    ASYNCRESET,
  output struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } y);

     struct packed {logic [7:0] x; logic y; } Register_inst0;	// <stdin>:2:10
  reg [5:0][15:0]                              Register_inst1;	// <stdin>:14:10
  reg [7:0]                                    Register_inst2;	// <stdin>:28:11

  always_ff @(posedge CLK or posedge ASYNCRESET) begin	// <stdin>:3:5
    if (ASYNCRESET) begin	// <stdin>:3:5
      automatic struct packed {logic [7:0] x; logic y; } _T = '{x: (8'hA), y: (1'h1)};	// <stdin>:10:10, :11:10, :12:10

      Register_inst0 <= _T;	// <stdin>:8:9
    end
    else begin	// <stdin>:3:5
      if (CE)	// <stdin>:4:9
        Register_inst0 <= a;	// <stdin>:5:13
    end
  end // always_ff @(posedge or posedge)
  always_ff @(posedge CLK) begin	// <stdin>:29:5
    Register_inst1 <= b;	// <stdin>:16:9
    if (CE)	// <stdin>:30:9
      Register_inst2 <= a.x;	// <stdin>:27:11, :31:13
  end // always_ff @(posedge)
  assign y = '{u: Register_inst0, v: Register_inst1};	// <stdin>:13:10, :25:10, :26:11, :36:5
endmodule


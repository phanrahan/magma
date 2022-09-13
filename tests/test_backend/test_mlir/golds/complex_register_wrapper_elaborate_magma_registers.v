module Register(	// <stdin>:1:1
  input  struct packed {logic [7:0] x; logic y; } I,
  input                                           CE, CLK, ASYNCRESET,
  output struct packed {logic [7:0] x; logic y; } O);

  wire [8:0] _T;	// <stdin>:35:10
  reg  [8:0] reg_PR9_inst0;	// <stdin>:25:11

  wire _T_8 = _T[8];	// <stdin>:10:11, :35:10
  always_ff @(posedge CLK or posedge ASYNCRESET) begin	// <stdin>:26:5
    if (ASYNCRESET)	// <stdin>:26:5
      reg_PR9_inst0 <= 9'h10A;	// <stdin>:29:9, :31:11
    else begin	// <stdin>:26:5
      automatic struct packed {logic [7:0] x; logic y; }      _T_0 = '{x: (reg_PR9_inst0[7:0]), y: _T_8};	// <stdin>:9:10, :11:11, :35:10
      automatic struct packed {logic [7:0] x; logic y; }[1:0] _T_1 = {{I}, {_T_0}};	// <stdin>:12:11
      automatic struct packed {logic [7:0] x; logic y; }      _T_2 = _T_1[CE];	// <stdin>:13:11

      reg_PR9_inst0 <= {_T_2.y, _T_2.x};	// <stdin>:14:11, :23:11, :24:11, :27:9
    end
  end // always_ff @(posedge or posedge)
  initial	// <stdin>:32:5
    reg_PR9_inst0 = 9'h10A;	// <stdin>:31:11, :33:9
  assign _T = reg_PR9_inst0;	// <stdin>:35:10
  assign O = '{x: (reg_PR9_inst0[7:0]), y: _T_8};	// <stdin>:35:10, :37:11, :38:11, :39:5
endmodule

module Register_unq1(	// <stdin>:41:1
  input  [5:0][15:0] I,
  input              CLK,
  output [5:0][15:0] O);

  reg [95:0] reg_P96_inst0;	// <stdin>:151:12

  always_ff @(posedge CLK)	// <stdin>:152:5
    reg_P96_inst0 <= {I[3'h5], I[3'h4], I[3'h3], I[3'h2], I[3'h1], I[3'h0]};	// <stdin>:42:10, :43:10, :60:11, :61:11, :78:11, :79:11, :96:11, :97:11, :114:11, :115:11, :132:11, :133:11, :150:12, :153:9
  initial	// <stdin>:156:5
    reg_P96_inst0 = 96'hA00080006000400020000;	// <stdin>:155:12, :157:9
  assign O = {{reg_P96_inst0[95:80]}, {reg_P96_inst0[79:64]}, {reg_P96_inst0[63:48]},
                {reg_P96_inst0[47:32]}, {reg_P96_inst0[31:16]}, {reg_P96_inst0[15:0]}};	// <stdin>:159:12, :176:12, :193:12, :210:12, :227:12, :244:12, :261:12, :262:12, :263:5
endmodule

module Register_unq2(	// <stdin>:265:1
  input  [7:0] I,
  input        CE, CLK,
  output [7:0] O);

  reg [7:0] reg_P8_inst0;	// <stdin>:268:10

  always_ff @(posedge CLK) begin	// <stdin>:269:5
    automatic logic [1:0][7:0] _T = {{I}, {reg_P8_inst0}};	// <stdin>:266:10, :276:10

    reg_P8_inst0 <= _T[CE];	// <stdin>:267:10, :270:9
  end // always_ff @(posedge)
  initial	// <stdin>:273:5
    reg_P8_inst0 = 8'h0;	// <stdin>:272:10, :274:9
  assign O = reg_P8_inst0;	// <stdin>:276:10, :277:5
endmodule

module complex_register_wrapper(	// <stdin>:279:1
  input  struct packed {logic [7:0] x; logic y; }                                          a,
  input  [5:0][15:0]                                                                       b,
  input                                                                                    CLK,
  input                                                                                    CE,
  input                                                                                    ASYNCRESET,
  output struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } y);

  wire [7:0]                                    Register_inst2_O;	// <stdin>:284:10
  wire [5:0][15:0]                              Register_inst1_O;	// <stdin>:281:10
  wire struct packed {logic [7:0] x; logic y; } Register_inst0_O;	// <stdin>:280:10

  Register Register_inst0 (	// <stdin>:280:10
    .I          (a),
    .CE         (CE),
    .CLK        (CLK),
    .ASYNCRESET (ASYNCRESET),
    .O          (Register_inst0_O)
  );
  Register_unq1 Register_inst1 (	// <stdin>:281:10
    .I   (b),
    .CLK (CLK),
    .O   (Register_inst1_O)
  );
  Register_unq2 Register_inst2 (	// <stdin>:284:10
    .I   (a.x),	// <stdin>:283:10
    .CE  (CE),
    .CLK (CLK),
    .O   (Register_inst2_O)
  );
  assign y = '{u: Register_inst0_O, v: Register_inst1_O};	// <stdin>:280:10, :281:10, :282:10, :285:5
endmodule


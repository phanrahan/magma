module complex_inline_verilog(	// <stdin>:1:1
  input  [11:0] I,
  input         CLK,
  output [11:0] O);

  reg  [11:0] Register_inst0;	// <stdin>:2:10
  wire        _magma_inline_wire0;	// <stdin>:12:10
  wire        _magma_inline_wire1;	// <stdin>:16:10
  wire        _magma_inline_wire2;	// <stdin>:20:11
  wire        _magma_inline_wire3;	// <stdin>:24:11
  wire        _magma_inline_wire4;	// <stdin>:28:11
  wire        _magma_inline_wire5;	// <stdin>:32:11
  wire        _magma_inline_wire6;	// <stdin>:36:11
  wire        _magma_inline_wire7;	// <stdin>:40:11
  wire        _magma_inline_wire8;	// <stdin>:44:11
  wire        _magma_inline_wire9;	// <stdin>:48:11
  wire        _magma_inline_wire10;	// <stdin>:52:11
  wire        _magma_inline_wire11;	// <stdin>:56:11
  wire        _magma_inline_wire12;	// <stdin>:60:11
  wire        _magma_inline_wire13;	// <stdin>:64:11
  wire        _magma_inline_wire14;	// <stdin>:68:11
  wire        _magma_inline_wire15;	// <stdin>:72:11
  wire        _magma_inline_wire16;	// <stdin>:76:11
  wire        _magma_inline_wire17;	// <stdin>:80:11
  wire        _magma_inline_wire18;	// <stdin>:84:11
  wire        _magma_inline_wire19;	// <stdin>:88:11
  wire        _magma_inline_wire20;	// <stdin>:92:11
  wire        _magma_inline_wire21;	// <stdin>:96:11
  wire        _magma_inline_wire22;	// <stdin>:100:11
  wire        _magma_inline_wire23;	// <stdin>:104:11
  wire [11:0] _magma_inline_wire24;	// <stdin>:108:11

  always_ff @(posedge CLK)	// <stdin>:3:5
    Register_inst0 <= I;	// <stdin>:4:9
  initial	// <stdin>:7:5
    Register_inst0 = 12'h0;	// <stdin>:6:10, :8:9
  assign _magma_inline_wire0 = I[0];	// <stdin>:11:10, :13:5
  assign _magma_inline_wire1 = Register_inst0[0];	// <stdin>:10:10, :15:10, :17:5
  assign _magma_inline_wire2 = I[1];	// <stdin>:19:10, :21:5
  assign _magma_inline_wire3 = Register_inst0[1];	// <stdin>:10:10, :23:11, :25:5
  assign _magma_inline_wire4 = I[2];	// <stdin>:27:11, :29:5
  assign _magma_inline_wire5 = Register_inst0[2];	// <stdin>:10:10, :31:11, :33:5
  assign _magma_inline_wire6 = I[3];	// <stdin>:35:11, :37:5
  assign _magma_inline_wire7 = Register_inst0[3];	// <stdin>:10:10, :39:11, :41:5
  assign _magma_inline_wire8 = I[4];	// <stdin>:43:11, :45:5
  assign _magma_inline_wire9 = Register_inst0[4];	// <stdin>:10:10, :47:11, :49:5
  assign _magma_inline_wire10 = I[5];	// <stdin>:51:11, :53:5
  assign _magma_inline_wire11 = Register_inst0[5];	// <stdin>:10:10, :55:11, :57:5
  assign _magma_inline_wire12 = I[6];	// <stdin>:59:11, :61:5
  assign _magma_inline_wire13 = Register_inst0[6];	// <stdin>:10:10, :63:11, :65:5
  assign _magma_inline_wire14 = I[7];	// <stdin>:67:11, :69:5
  assign _magma_inline_wire15 = Register_inst0[7];	// <stdin>:10:10, :71:11, :73:5
  assign _magma_inline_wire16 = I[8];	// <stdin>:75:11, :77:5
  assign _magma_inline_wire17 = Register_inst0[8];	// <stdin>:10:10, :79:11, :81:5
  assign _magma_inline_wire18 = I[9];	// <stdin>:83:11, :85:5
  assign _magma_inline_wire19 = Register_inst0[9];	// <stdin>:10:10, :87:11, :89:5
  assign _magma_inline_wire20 = I[10];	// <stdin>:91:11, :93:5
  assign _magma_inline_wire21 = Register_inst0[10];	// <stdin>:10:10, :95:11, :97:5
  assign _magma_inline_wire22 = I[11];	// <stdin>:99:11, :101:5
  assign _magma_inline_wire23 = Register_inst0[11];	// <stdin>:10:10, :103:11, :105:5
  assert property (@(posedge CLK) _magma_inline_wire0 |-> ##1 _magma_inline_wire1);
  assert property (@(posedge CLK) _magma_inline_wire2 |-> ##1 _magma_inline_wire3);
  assert property (@(posedge CLK) _magma_inline_wire4 |-> ##1 _magma_inline_wire5);
  assert property (@(posedge CLK) _magma_inline_wire6 |-> ##1 _magma_inline_wire7);
  assert property (@(posedge CLK) _magma_inline_wire8 |-> ##1 _magma_inline_wire9);
  assert property (@(posedge CLK) _magma_inline_wire10 |-> ##1 _magma_inline_wire11);
  assert property (@(posedge CLK) _magma_inline_wire12 |-> ##1 _magma_inline_wire13);
  assert property (@(posedge CLK) _magma_inline_wire14 |-> ##1 _magma_inline_wire15);
  assert property (@(posedge CLK) _magma_inline_wire16 |-> ##1 _magma_inline_wire17);
  assert property (@(posedge CLK) _magma_inline_wire18 |-> ##1 _magma_inline_wire19);
  assert property (@(posedge CLK) _magma_inline_wire20 |-> ##1 _magma_inline_wire21);
  assert property (@(posedge CLK) _magma_inline_wire22 |-> ##1 _magma_inline_wire23);	// <stdin>:14:10, :18:10, :22:11, :26:11, :30:11, :34:11, :38:11, :42:11, :46:11, :50:11, :54:11, :58:11, :62:11, :66:11, :70:11, :74:11, :78:11, :82:11, :86:11, :90:11, :94:11, :98:11, :102:11, :106:11, :107:5
  assign _magma_inline_wire24 = I;	// <stdin>:109:5
  // A fun{k}y comment with _magma_inline_wire24	// <stdin>:110:11, :111:5
  assign O = Register_inst0;	// <stdin>:10:10, :112:5
endmodule


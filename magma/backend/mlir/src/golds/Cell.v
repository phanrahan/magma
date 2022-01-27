module Cell(	// <stdin>:1:1
  input  [7:0] neighbors,
  input        running, write_enable, write_value, CLK,
  output       out);

  reg Register_inst0;	// <stdin>:70:11

  always_ff @(posedge CLK) begin	// <stdin>:71:5
    automatic logic [2:0] _T = {2'h0, neighbors[0]} + {2'h0, neighbors[1]} + {2'h0, neighbors[2]} + {2'h0, neighbors[3]} +
                                {2'h0, neighbors[4]} + {2'h0, neighbors[5]} + {2'h0, neighbors[6]} + {2'h0, neighbors[7]};	// <stdin>:7:10, :10:10, :12:11, :15:11, :17:11, :20:11, :22:11, :25:11, :27:11, :30:11, :32:11, :35:11, :37:11, :40:11, :42:11, :45:11, :46:11
    automatic logic [1:0] _T_0 = {{Register_inst0}, {write_value}};	// <stdin>:65:11, :78:10
    automatic logic [1:0] _T_1 = {{1'h0}, {1'h1}};	// <stdin>:2:10, :3:10, :56:11
    automatic logic [1:0] _T_2 = {{_T_1[~(_T[2])]}, {1'h0}};	// <stdin>:2:10, :55:11, :57:11, :61:11
    automatic logic [1:0] _T_3 = {{1'h0}, {1'h1}};	// <stdin>:2:10, :3:10, :50:11
    automatic logic [1:0] _T_4 = {{_T_3[~Register_inst0 & _T == 3'h3]}, {_T_2[_T < 3'h2]}};	// <stdin>:5:10, :47:11, :48:11, :49:11, :51:11, :59:11, :60:11, :62:11, :63:11, :78:10
    automatic logic [1:0] _T_5 = {{_T_4[Register_inst0]}, {_T_0[write_enable]}};	// <stdin>:64:11, :66:11, :68:11, :78:10

    Register_inst0 <= _T_5[~running];	// <stdin>:67:11, :69:11, :72:9
  end // always_ff @(posedge)
  initial	// <stdin>:75:5
    Register_inst0 = 1'h0;	// <stdin>:2:10, :76:9
  assign out = Register_inst0;	// <stdin>:78:10, :79:5
endmodule


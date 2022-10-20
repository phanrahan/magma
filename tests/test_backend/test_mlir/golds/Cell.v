module Cell(
  input  [7:0] neighbors,
  input        running, write_enable, write_value, CLK,
  output       out);

  reg Register_inst0;

  always_ff @(posedge CLK) begin
    automatic logic [2:0] _T = {2'h0, neighbors[0]} + {2'h0, neighbors[1]} + {2'h0, neighbors[2]} + {2'h0, neighbors[3]} +
                                {2'h0, neighbors[4]} + {2'h0, neighbors[5]} + {2'h0, neighbors[6]} + {2'h0, neighbors[7]};
    automatic logic [1:0] _T_0 = {{Register_inst0}, {write_value}};
    automatic logic [1:0] _T_1 = {{1'h0}, {1'h1}};
    automatic logic [1:0] _T_2 = {{_T_1[~(_T[2])]}, {1'h0}};
    automatic logic [1:0] _T_3 = {{1'h0}, {1'h1}};
    automatic logic [1:0] _T_4 = {{_T_3[~Register_inst0 & _T == 3'h3]}, {_T_2[_T < 3'h2]}};
    automatic logic [1:0] _T_5 = {{_T_4[Register_inst0]}, {_T_0[write_enable]}};

    Register_inst0 <= _T_5[~running];
  end // always_ff @(posedge)
  initial
    Register_inst0 = 1'h0;
  assign out = Register_inst0;
endmodule


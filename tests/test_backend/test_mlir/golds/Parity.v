module Parity(
  input  I, CLK,
  output O);

  reg Register_inst0;

  always_ff @(posedge CLK) begin
    automatic logic [1:0] _T = {{1'h0}, {1'h1}};
    automatic logic [1:0] _T_0 = {{Register_inst0}, {_T[~Register_inst0]}};

    Register_inst0 <= _T_0[I];
  end // always_ff @(posedge)
  initial
    Register_inst0 = 1'h0;
  assign O = Register_inst0;
endmodule


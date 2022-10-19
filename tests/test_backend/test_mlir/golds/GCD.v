module GCD(
  input  [15:0] a, b,
  input         load, CLK,
  output [15:0] O0,
  output        O1);

  reg [15:0] Register_inst1;
  reg [15:0] Register_inst0;

  always_ff @(posedge CLK) begin
    automatic logic             _T = Register_inst1 < Register_inst0;
    automatic logic [1:0][15:0] _T_0 = {{Register_inst1 - Register_inst0}, {Register_inst1}};
    automatic logic [1:0][15:0] _T_1 = {{Register_inst1}, {_T_0[_T]}};
    automatic logic [1:0][15:0] _T_2 = {{_T_1[|Register_inst1]}, {b}};
    automatic logic [1:0][15:0] _T_3 = {{Register_inst0}, {Register_inst0 - Register_inst1}};
    automatic logic [1:0][15:0] _T_4 = {{Register_inst0}, {_T_3[_T]}};
    automatic logic [1:0][15:0] _T_5 = {{_T_4[|Register_inst1]}, {a}};

    Register_inst1 <= _T_2[load];
    Register_inst0 <= _T_5[load];
  end // always_ff @(posedge)
  initial begin
    Register_inst1 = 16'h0;
    Register_inst0 = 16'h0;
  end // initial
  assign O0 = Register_inst0;
  assign O1 = Register_inst1 == 16'h0;
endmodule


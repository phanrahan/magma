module LogShifter(
  input  [15:0] I,
  input  [3:0]  shift_amount,
  input         CLK,
  output [15:0] O);

  reg [15:0] Register_inst0;
  reg [15:0] Register_inst1;
  reg [15:0] Register_inst2;

  always_ff @(posedge CLK) begin
    automatic logic [1:0][15:0] _T_0 = {{I}, {{I[7:0], 8'h0}}};
    automatic logic [1:0][15:0] _T_1 = {{Register_inst0}, {{Register_inst0[11:0], 4'h0}}};
    automatic logic [1:0][15:0] _T_2 = {{Register_inst1}, {{Register_inst1[13:0], 2'h0}}};

    Register_inst0 <= _T_0[shift_amount[3]];
    Register_inst1 <= _T_1[shift_amount[2]];
    Register_inst2 <= _T_2[shift_amount[1]];
  end // always_ff @(posedge)
  initial begin
    Register_inst0 = 16'h0;
    Register_inst1 = 16'h0;
    Register_inst2 = 16'h0;
  end // initial
  wire [1:0][15:0] _T = {{Register_inst2}, {{Register_inst2[14:0], 1'h0}}};
  assign O = _T[shift_amount[0]];
endmodule


module ShiftRegister(
  input  I, CLK,
  output O);

  reg Register_inst0;
  reg Register_inst1;
  reg Register_inst2;
  reg Register_inst3;

  always_ff @(posedge CLK) begin
    Register_inst0 <= I;
    Register_inst1 <= Register_inst0;
    Register_inst2 <= Register_inst1;
    Register_inst3 <= Register_inst2;
  end // always_ff @(posedge)
  initial begin
    Register_inst0 = 1'h0;
    Register_inst1 = 1'h0;
    Register_inst2 = 1'h0;
    Register_inst3 = 1'h0;
  end // initial
  assign O = Register_inst3;
endmodule


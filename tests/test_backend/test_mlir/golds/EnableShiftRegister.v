module EnableShiftRegister(
  input  [3:0] I,
  input        shift, CLK, ASYNCRESET,
  output [3:0] O);

  reg [3:0] Register_inst0;
  reg [3:0] Register_inst1;
  reg [3:0] Register_inst2;
  reg [3:0] Register_inst3;

  always_ff @(posedge CLK or posedge ASYNCRESET) begin
    if (ASYNCRESET) begin
      Register_inst0 <= 4'h0;
      Register_inst1 <= 4'h0;
      Register_inst2 <= 4'h0;
      Register_inst3 <= 4'h0;
    end
    else begin
      if (shift)
        Register_inst0 <= I;
      if (shift)
        Register_inst1 <= Register_inst0;
      if (shift)
        Register_inst2 <= Register_inst1;
      if (shift)
        Register_inst3 <= Register_inst2;
    end
  end // always_ff @(posedge or posedge)
  initial begin
    Register_inst0 = 4'h0;
    Register_inst1 = 4'h0;
    Register_inst2 = 4'h0;
    Register_inst3 = 4'h0;
  end // initial
  assign O = Register_inst3;
endmodule


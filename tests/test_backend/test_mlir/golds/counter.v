// Generated by CIRCT firtool-1.48.0-34-g7018fb13b
module counter(
  input         CLK,
  output [15:0] y
);

  reg [15:0] Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= Register_inst0 + 16'h1;
  initial
    Register_inst0 = 16'h0;
  assign y = Register_inst0;
endmodule


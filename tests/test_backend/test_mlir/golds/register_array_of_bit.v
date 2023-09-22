module register_array_of_bit(
  input  [3:0] I,
  input        CLK,
  output [3:0] O
);

  reg [3:0] Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= I;
  initial
    Register_inst0 = 4'h3;
  assign O = Register_inst0;
endmodule


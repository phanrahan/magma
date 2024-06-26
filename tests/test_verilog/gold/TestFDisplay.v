module TestFDisplay(
  input  I,
         CLK,
         CE,
  output O
);

  reg ff;
  always_ff @(posedge CLK) begin
    if (CE)
      ff <= I;
  end // always_ff @(posedge)
  initial
    ff = 1'h0;

  integer \_file_test_fdisplay.log ;
  initial \_file_test_fdisplay.log = $fopen("test_fdisplay.log", "a");
  always @(posedge CLK) begin
      if (CE) $fdisplay(\_file_test_fdisplay.log , "ff.O=%d, ff.I=%d", ff, I);
  end

  final $fclose(\_file_test_fdisplay.log );
  assign O = ff;
endmodule


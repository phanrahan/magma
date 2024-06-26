module TestFLog(
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

  `ifndef MAGMA_LOG_LEVEL
      `define MAGMA_LOG_LEVEL 1
  `endif

  integer \_file_test_flog.log ;
  initial \_file_test_flog.log = $fopen("test_flog.log", "a");
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 0) && (CE)) $fdisplay(\_file_test_flog.log , "[DEBUG] ff.O=%d, ff.I=%d", ff, I);
  end
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 1) && (CE)) $fdisplay(\_file_test_flog.log , "[INFO] ff.O=%d, ff.I=%d", ff, I);
  end
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 2) && (CE)) $fdisplay(\_file_test_flog.log , "[WARNING] ff.O=%d, ff.I=%d", ff, I);
  end
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 3) && (CE)) $fdisplay(\_file_test_flog.log , "[ERROR] ff.O=%d, ff.I=%d", ff, I);
  end

  final $fclose(\_file_test_flog.log );
  assign O = ff;
endmodule


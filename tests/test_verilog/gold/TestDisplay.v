module TestDisplay(
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
  always @(posedge CLK) begin
      if (CE) $display("%0t: ff.O=%d, ff.I=%d", $time, ff, I);
  end
  assign O = ff;
endmodule


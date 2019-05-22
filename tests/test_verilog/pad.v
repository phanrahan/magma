module PRWDWUWSWCDGH_V (C, DS0, DS1, DS2, I, IE, OEN, PAD, PU, PD, ST, SL, RTE);

  input  DS0, DS1, DS2, I, IE, OEN, PU, PD, ST, SL, RTE;
  output C;
  inout  PAD;

  assign C = PAD;

  assign pad = ((IE == 1'b0) & (OEN ==1'b0)) ? I : 1'bz;

endmodule

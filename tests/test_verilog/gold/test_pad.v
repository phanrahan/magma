module corebit_const #(parameter value=1) (
  output out
);
  assign out = value;

endmodule  // corebit_const

/* External Modules
module PRWDWUWSWCDGH_V (
  output  C,
  input  DS0,
  input  DS1,
  input  DS2,
  input  I,
  input  IE,
  input  OEN,
  inout  PAD,
  input  PD,
  input  PU,
  input  RTE,
  input  SL,
  input  ST
);

endmodule  // PRWDWUWSWCDGH_V

*/
module Top (
  inout  pad
);


  wire  PRWDWUWSWCDGH_V_inst0__C;
  wire  PRWDWUWSWCDGH_V_inst0__DS0;
  wire  PRWDWUWSWCDGH_V_inst0__DS1;
  wire  PRWDWUWSWCDGH_V_inst0__DS2;
  wire  PRWDWUWSWCDGH_V_inst0__I;
  wire  PRWDWUWSWCDGH_V_inst0__IE;
  wire  PRWDWUWSWCDGH_V_inst0__OEN;
  wire  PRWDWUWSWCDGH_V_inst0__PAD;
  wire  PRWDWUWSWCDGH_V_inst0__PD;
  wire  PRWDWUWSWCDGH_V_inst0__PU;
  wire  PRWDWUWSWCDGH_V_inst0__RTE;
  wire  PRWDWUWSWCDGH_V_inst0__SL;
  wire  PRWDWUWSWCDGH_V_inst0__ST;
  PRWDWUWSWCDGH_V PRWDWUWSWCDGH_V_inst0(
    .C(PRWDWUWSWCDGH_V_inst0__C),
    .DS0(PRWDWUWSWCDGH_V_inst0__DS0),
    .DS1(PRWDWUWSWCDGH_V_inst0__DS1),
    .DS2(PRWDWUWSWCDGH_V_inst0__DS2),
    .I(PRWDWUWSWCDGH_V_inst0__I),
    .IE(PRWDWUWSWCDGH_V_inst0__IE),
    .OEN(PRWDWUWSWCDGH_V_inst0__OEN),
    .PAD(PRWDWUWSWCDGH_V_inst0__PAD),
    .PD(PRWDWUWSWCDGH_V_inst0__PD),
    .PU(PRWDWUWSWCDGH_V_inst0__PU),
    .RTE(PRWDWUWSWCDGH_V_inst0__RTE),
    .SL(PRWDWUWSWCDGH_V_inst0__SL),
    .ST(PRWDWUWSWCDGH_V_inst0__ST)
  );

  wire  bit_const_0_None__out;
  corebit_const #(.value(0)) bit_const_0_None(
    .out(bit_const_0_None__out)
  );

  assign PRWDWUWSWCDGH_V_inst0__DS0 = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__DS1 = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__DS2 = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__I = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__IE = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__OEN = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__PAD = pad;

  assign PRWDWUWSWCDGH_V_inst0__PD = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__PU = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__RTE = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__SL = bit_const_0_None__out;

  assign PRWDWUWSWCDGH_V_inst0__ST = bit_const_0_None__out;


endmodule  // Top


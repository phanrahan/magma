module coreir_mul #(parameter width=1) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);
  assign out = in0 * in1;

endmodule  // coreir_mul

module MulFixed (
  output [42:0] o,
  input [17:0] u,
  input [24:0] x
);


  // Instancing generated Module: coreir.mul(width:43)
  wire [42:0] coreir_mul_inst0__in0;
  wire [42:0] coreir_mul_inst0__in1;
  wire [42:0] coreir_mul_inst0__out;
  coreir_mul #(.width(43)) coreir_mul_inst0(
    .in0(coreir_mul_inst0__in0),
    .in1(coreir_mul_inst0__in1),
    .out(coreir_mul_inst0__out)
  );

  assign coreir_mul_inst0__in0[0] = u[0];

  assign coreir_mul_inst0__in0[10] = u[10];

  assign coreir_mul_inst0__in0[11] = u[11];

  assign coreir_mul_inst0__in0[12] = u[12];

  assign coreir_mul_inst0__in0[13] = u[13];

  assign coreir_mul_inst0__in0[14] = u[14];

  assign coreir_mul_inst0__in0[15] = u[15];

  assign coreir_mul_inst0__in0[16] = u[16];

  assign coreir_mul_inst0__in0[17] = u[17];

  assign coreir_mul_inst0__in0[18] = u[17];

  assign coreir_mul_inst0__in0[19] = u[17];

  assign coreir_mul_inst0__in0[1] = u[1];

  assign coreir_mul_inst0__in0[20] = u[17];

  assign coreir_mul_inst0__in0[21] = u[17];

  assign coreir_mul_inst0__in0[22] = u[17];

  assign coreir_mul_inst0__in0[23] = u[17];

  assign coreir_mul_inst0__in0[24] = u[17];

  assign coreir_mul_inst0__in0[25] = u[17];

  assign coreir_mul_inst0__in0[26] = u[17];

  assign coreir_mul_inst0__in0[27] = u[17];

  assign coreir_mul_inst0__in0[28] = u[17];

  assign coreir_mul_inst0__in0[29] = u[17];

  assign coreir_mul_inst0__in0[2] = u[2];

  assign coreir_mul_inst0__in0[30] = u[17];

  assign coreir_mul_inst0__in0[31] = u[17];

  assign coreir_mul_inst0__in0[32] = u[17];

  assign coreir_mul_inst0__in0[33] = u[17];

  assign coreir_mul_inst0__in0[34] = u[17];

  assign coreir_mul_inst0__in0[35] = u[17];

  assign coreir_mul_inst0__in0[36] = u[17];

  assign coreir_mul_inst0__in0[37] = u[17];

  assign coreir_mul_inst0__in0[38] = u[17];

  assign coreir_mul_inst0__in0[39] = u[17];

  assign coreir_mul_inst0__in0[3] = u[3];

  assign coreir_mul_inst0__in0[40] = u[17];

  assign coreir_mul_inst0__in0[41] = u[17];

  assign coreir_mul_inst0__in0[42] = u[17];

  assign coreir_mul_inst0__in0[4] = u[4];

  assign coreir_mul_inst0__in0[5] = u[5];

  assign coreir_mul_inst0__in0[6] = u[6];

  assign coreir_mul_inst0__in0[7] = u[7];

  assign coreir_mul_inst0__in0[8] = u[8];

  assign coreir_mul_inst0__in0[9] = u[9];

  assign coreir_mul_inst0__in1[0] = x[0];

  assign coreir_mul_inst0__in1[10] = x[10];

  assign coreir_mul_inst0__in1[11] = x[11];

  assign coreir_mul_inst0__in1[12] = x[12];

  assign coreir_mul_inst0__in1[13] = x[13];

  assign coreir_mul_inst0__in1[14] = x[14];

  assign coreir_mul_inst0__in1[15] = x[15];

  assign coreir_mul_inst0__in1[16] = x[16];

  assign coreir_mul_inst0__in1[17] = x[17];

  assign coreir_mul_inst0__in1[18] = x[18];

  assign coreir_mul_inst0__in1[19] = x[19];

  assign coreir_mul_inst0__in1[1] = x[1];

  assign coreir_mul_inst0__in1[20] = x[20];

  assign coreir_mul_inst0__in1[21] = x[21];

  assign coreir_mul_inst0__in1[22] = x[22];

  assign coreir_mul_inst0__in1[23] = x[23];

  assign coreir_mul_inst0__in1[24] = x[24];

  assign coreir_mul_inst0__in1[25] = x[24];

  assign coreir_mul_inst0__in1[26] = x[24];

  assign coreir_mul_inst0__in1[27] = x[24];

  assign coreir_mul_inst0__in1[28] = x[24];

  assign coreir_mul_inst0__in1[29] = x[24];

  assign coreir_mul_inst0__in1[2] = x[2];

  assign coreir_mul_inst0__in1[30] = x[24];

  assign coreir_mul_inst0__in1[31] = x[24];

  assign coreir_mul_inst0__in1[32] = x[24];

  assign coreir_mul_inst0__in1[33] = x[24];

  assign coreir_mul_inst0__in1[34] = x[24];

  assign coreir_mul_inst0__in1[35] = x[24];

  assign coreir_mul_inst0__in1[36] = x[24];

  assign coreir_mul_inst0__in1[37] = x[24];

  assign coreir_mul_inst0__in1[38] = x[24];

  assign coreir_mul_inst0__in1[39] = x[24];

  assign coreir_mul_inst0__in1[3] = x[3];

  assign coreir_mul_inst0__in1[40] = x[24];

  assign coreir_mul_inst0__in1[41] = x[24];

  assign coreir_mul_inst0__in1[42] = x[24];

  assign coreir_mul_inst0__in1[4] = x[4];

  assign coreir_mul_inst0__in1[5] = x[5];

  assign coreir_mul_inst0__in1[6] = x[6];

  assign coreir_mul_inst0__in1[7] = x[7];

  assign coreir_mul_inst0__in1[8] = x[8];

  assign coreir_mul_inst0__in1[9] = x[9];

  assign o[42:0] = coreir_mul_inst0__out[42:0];


endmodule  // MulFixed


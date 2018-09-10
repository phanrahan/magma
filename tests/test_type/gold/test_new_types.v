

module TestCircuit (
  input [2:0] I_0_x,
  input [2:0] I_0_y,
  input [2:0] I_10_x,
  input [2:0] I_10_y,
  input [2:0] I_11_x,
  input [2:0] I_11_y,
  input [2:0] I_1_x,
  input [2:0] I_1_y,
  input [2:0] I_2_x,
  input [2:0] I_2_y,
  input [2:0] I_3_x,
  input [2:0] I_3_y,
  input [2:0] I_4_x,
  input [2:0] I_4_y,
  input [2:0] I_5_x,
  input [2:0] I_5_y,
  input [2:0] I_6_x,
  input [2:0] I_6_y,
  input [2:0] I_7_x,
  input [2:0] I_7_y,
  input [2:0] I_8_x,
  input [2:0] I_8_y,
  input [2:0] I_9_x,
  input [2:0] I_9_y,
  output [2:0] O_0_x,
  output [2:0] O_0_y,
  output [2:0] O_10_x,
  output [2:0] O_10_y,
  output [2:0] O_11_x,
  output [2:0] O_11_y,
  output [2:0] O_1_x,
  output [2:0] O_1_y,
  output [2:0] O_2_x,
  output [2:0] O_2_y,
  output [2:0] O_3_x,
  output [2:0] O_3_y,
  output [2:0] O_4_x,
  output [2:0] O_4_y,
  output [2:0] O_5_x,
  output [2:0] O_5_y,
  output [2:0] O_6_x,
  output [2:0] O_6_y,
  output [2:0] O_7_x,
  output [2:0] O_7_y,
  output [2:0] O_8_x,
  output [2:0] O_8_y,
  output [2:0] O_9_x,
  output [2:0] O_9_y
);
  //All the connections
  assign O_0_x[2:0] = I_0_x[2:0];
  assign O_0_y[2:0] = I_0_y[2:0];
  assign O_1_x[2:0] = I_1_x[2:0];
  assign O_1_y[2:0] = I_1_y[2:0];
  assign O_2_x[2:0] = I_2_x[2:0];
  assign O_2_y[2:0] = I_2_y[2:0];
  assign O_3_x[2:0] = I_3_x[2:0];
  assign O_3_y[2:0] = I_3_y[2:0];
  assign O_4_x[2:0] = I_4_x[2:0];
  assign O_4_y[2:0] = I_4_y[2:0];
  assign O_5_x[2:0] = I_5_x[2:0];
  assign O_5_y[2:0] = I_5_y[2:0];
  assign O_6_x[2:0] = I_6_x[2:0];
  assign O_6_y[2:0] = I_6_y[2:0];
  assign O_7_x[2:0] = I_7_x[2:0];
  assign O_7_y[2:0] = I_7_y[2:0];
  assign O_8_x[2:0] = I_8_x[2:0];
  assign O_8_y[2:0] = I_8_y[2:0];
  assign O_9_x[2:0] = I_9_x[2:0];
  assign O_9_y[2:0] = I_9_y[2:0];
  assign O_10_x[2:0] = I_10_x[2:0];
  assign O_10_y[2:0] = I_10_y[2:0];
  assign O_11_x[2:0] = I_11_x[2:0];
  assign O_11_y[2:0] = I_11_y[2:0];

endmodule //TestCircuit

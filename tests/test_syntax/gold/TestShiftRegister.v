module coreir_reg #(parameter clk_posedge=1, parameter init=1, parameter width=1) (
  input clk,
  input [width-1:0] in,
  output [width-1:0] out
);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;

endmodule  // coreir_reg

module TestShiftRegister_comb (
  input [1:0] I,
  output [1:0] O0,
  output [1:0] O1,
  output [1:0] O2,
  input [1:0] self_x_O,
  input [1:0] self_y_O
);


  assign O0[1:0] = I[1:0];

  assign O1[1:0] = self_x_O[1:0];

  assign O2[1:0] = self_y_O[1:0];


endmodule  // TestShiftRegister_comb

module Register_comb (
  input [1:0] I,
  output [1:0] O0,
  output [1:0] O1,
  input [1:0] self_value_O
);


  assign O0[1:0] = I[1:0];

  assign O1[1:0] = self_value_O[1:0];


endmodule  // Register_comb

module Register_unq1 (
  input  CLK,
  input [1:0] I,
  output [1:0] O
);


  wire [1:0] Register_comb_inst0__I;
  wire [1:0] Register_comb_inst0__O0;
  wire [1:0] Register_comb_inst0__O1;
  wire [1:0] Register_comb_inst0__self_value_O;
  Register_comb Register_comb_inst0(
    .I(Register_comb_inst0__I),
    .O0(Register_comb_inst0__O0),
    .O1(Register_comb_inst0__O1),
    .self_value_O(Register_comb_inst0__self_value_O)
  );

  // Instancing generated Module: coreir.reg(width:2)
  wire  reg_P_inst0__clk;
  wire [1:0] reg_P_inst0__in;
  wire [1:0] reg_P_inst0__out;
  coreir_reg #(.clk_posedge(1),.init(2'h1),.width(2)) reg_P_inst0(
    .clk(reg_P_inst0__clk),
    .in(reg_P_inst0__in),
    .out(reg_P_inst0__out)
  );

  assign Register_comb_inst0__I[1:0] = I[1:0];

  assign reg_P_inst0__in[1:0] = Register_comb_inst0__O0[1:0];

  assign O[1:0] = Register_comb_inst0__O1[1:0];

  assign Register_comb_inst0__self_value_O[1:0] = reg_P_inst0__out[1:0];

  assign reg_P_inst0__clk = CLK;


endmodule  // Register_unq1

module Register (
  input  CLK,
  input [1:0] I,
  output [1:0] O
);


  wire [1:0] Register_comb_inst0__I;
  wire [1:0] Register_comb_inst0__O0;
  wire [1:0] Register_comb_inst0__O1;
  wire [1:0] Register_comb_inst0__self_value_O;
  Register_comb Register_comb_inst0(
    .I(Register_comb_inst0__I),
    .O0(Register_comb_inst0__O0),
    .O1(Register_comb_inst0__O1),
    .self_value_O(Register_comb_inst0__self_value_O)
  );

  // Instancing generated Module: coreir.reg(width:2)
  wire  reg_P_inst0__clk;
  wire [1:0] reg_P_inst0__in;
  wire [1:0] reg_P_inst0__out;
  coreir_reg #(.clk_posedge(1),.init(2'h0),.width(2)) reg_P_inst0(
    .clk(reg_P_inst0__clk),
    .in(reg_P_inst0__in),
    .out(reg_P_inst0__out)
  );

  assign Register_comb_inst0__I[1:0] = I[1:0];

  assign reg_P_inst0__in[1:0] = Register_comb_inst0__O0[1:0];

  assign O[1:0] = Register_comb_inst0__O1[1:0];

  assign Register_comb_inst0__self_value_O[1:0] = reg_P_inst0__out[1:0];

  assign reg_P_inst0__clk = CLK;


endmodule  // Register

module TestShiftRegister (
  input  CLK,
  input [1:0] I,
  output [1:0] O
);


  wire  Register_inst0__CLK;
  wire [1:0] Register_inst0__I;
  wire [1:0] Register_inst0__O;
  Register Register_inst0(
    .CLK(Register_inst0__CLK),
    .I(Register_inst0__I),
    .O(Register_inst0__O)
  );

  wire  Register_inst1__CLK;
  wire [1:0] Register_inst1__I;
  wire [1:0] Register_inst1__O;
  Register_unq1 Register_inst1(
    .CLK(Register_inst1__CLK),
    .I(Register_inst1__I),
    .O(Register_inst1__O)
  );

  wire [1:0] TestShiftRegister_comb_inst0__I;
  wire [1:0] TestShiftRegister_comb_inst0__O0;
  wire [1:0] TestShiftRegister_comb_inst0__O1;
  wire [1:0] TestShiftRegister_comb_inst0__O2;
  wire [1:0] TestShiftRegister_comb_inst0__self_x_O;
  wire [1:0] TestShiftRegister_comb_inst0__self_y_O;
  TestShiftRegister_comb TestShiftRegister_comb_inst0(
    .I(TestShiftRegister_comb_inst0__I),
    .O0(TestShiftRegister_comb_inst0__O0),
    .O1(TestShiftRegister_comb_inst0__O1),
    .O2(TestShiftRegister_comb_inst0__O2),
    .self_x_O(TestShiftRegister_comb_inst0__self_x_O),
    .self_y_O(TestShiftRegister_comb_inst0__self_y_O)
  );

  assign Register_inst0__CLK = CLK;

  assign Register_inst0__I[1:0] = TestShiftRegister_comb_inst0__O0[1:0];

  assign TestShiftRegister_comb_inst0__self_x_O[1:0] = Register_inst0__O[1:0];

  assign Register_inst1__CLK = CLK;

  assign Register_inst1__I[1:0] = TestShiftRegister_comb_inst0__O1[1:0];

  assign TestShiftRegister_comb_inst0__self_y_O[1:0] = Register_inst1__O[1:0];

  assign TestShiftRegister_comb_inst0__I[1:0] = I[1:0];

  assign O[1:0] = TestShiftRegister_comb_inst0__O2[1:0];


endmodule  // TestShiftRegister


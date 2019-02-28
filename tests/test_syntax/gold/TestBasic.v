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

module TestBasic_comb (
  input [1:0] I,
  output [1:0] O0,
  output [1:0] O1,
  output [1:0] O2,
  input [1:0] self_x,
  input [1:0] self_y
);


  assign O0[1:0] = I[1:0];

  assign O1[1:0] = self_x[1:0];

  assign O2[1:0] = self_y[1:0];


endmodule  // TestBasic_comb

module TestBasic (
  input  CLK,
  input [1:0] I,
  output [1:0] O
);


  wire [1:0] TestBasic_comb_inst0__I;
  wire [1:0] TestBasic_comb_inst0__O0;
  wire [1:0] TestBasic_comb_inst0__O1;
  wire [1:0] TestBasic_comb_inst0__O2;
  wire [1:0] TestBasic_comb_inst0__self_x;
  wire [1:0] TestBasic_comb_inst0__self_y;
  TestBasic_comb TestBasic_comb_inst0(
    .I(TestBasic_comb_inst0__I),
    .O0(TestBasic_comb_inst0__O0),
    .O1(TestBasic_comb_inst0__O1),
    .O2(TestBasic_comb_inst0__O2),
    .self_x(TestBasic_comb_inst0__self_x),
    .self_y(TestBasic_comb_inst0__self_y)
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

  // Instancing generated Module: coreir.reg(width:2)
  wire  reg_P_inst1__clk;
  wire [1:0] reg_P_inst1__in;
  wire [1:0] reg_P_inst1__out;
  coreir_reg #(.clk_posedge(1),.init(2'h0),.width(2)) reg_P_inst1(
    .clk(reg_P_inst1__clk),
    .in(reg_P_inst1__in),
    .out(reg_P_inst1__out)
  );

  assign TestBasic_comb_inst0__I[1:0] = I[1:0];

  assign reg_P_inst0__in[1:0] = TestBasic_comb_inst0__O0[1:0];

  assign reg_P_inst1__in[1:0] = TestBasic_comb_inst0__O1[1:0];

  assign O[1:0] = TestBasic_comb_inst0__O2[1:0];

  assign TestBasic_comb_inst0__self_x[1:0] = reg_P_inst0__out[1:0];

  assign TestBasic_comb_inst0__self_y[1:0] = reg_P_inst1__out[1:0];

  assign reg_P_inst0__clk = CLK;

  assign reg_P_inst1__clk = CLK;


endmodule  // TestBasic


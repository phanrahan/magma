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

module coreir_eq #(parameter width=1) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  output out
);
  assign out = in0 == in1;

endmodule  // coreir_eq

module coreir_const #(parameter value=1, parameter width=1) (
  output [width-1:0] out
);
  assign out = value;

endmodule  // coreir_const

module corebit_const #(parameter value=1) (
  output out
);
  assign out = value;

endmodule  // corebit_const

module corebit_and (
  input in0,
  input in1,
  output out
);
  assign out = in0 & in1;

endmodule  // corebit_and

/* External Modules
module Mux2_x4 (
  input [3:0] I0,
  input [3:0] I1,
  output [3:0] O,
  input  S
);

endmodule  // Mux2_x4

*/
module Register_comb (
  output [3:0] O0,
  output [3:0] O1,
  input  en,
  input [3:0] self_value_O,
  input [3:0] value
);


  wire [3:0] Mux2_x4_inst0__I0;
  wire [3:0] Mux2_x4_inst0__I1;
  wire [3:0] Mux2_x4_inst0__O;
  wire  Mux2_x4_inst0__S;
  Mux2_x4 Mux2_x4_inst0(
    .I0(Mux2_x4_inst0__I0),
    .I1(Mux2_x4_inst0__I1),
    .O(Mux2_x4_inst0__O),
    .S(Mux2_x4_inst0__S)
  );

  assign Mux2_x4_inst0__I0[3:0] = self_value_O[3:0];

  assign Mux2_x4_inst0__I1[3:0] = value[3:0];

  assign O0[3:0] = Mux2_x4_inst0__O[3:0];

  assign Mux2_x4_inst0__S = en;

  assign O1[3:0] = self_value_O[3:0];


endmodule  // Register_comb

module Register (
  input  CLK,
  output [3:0] O,
  input  en,
  input [3:0] value
);


  wire [3:0] Register_comb_inst0__O0;
  wire [3:0] Register_comb_inst0__O1;
  wire  Register_comb_inst0__en;
  wire [3:0] Register_comb_inst0__self_value_O;
  wire [3:0] Register_comb_inst0__value;
  Register_comb Register_comb_inst0(
    .O0(Register_comb_inst0__O0),
    .O1(Register_comb_inst0__O1),
    .en(Register_comb_inst0__en),
    .self_value_O(Register_comb_inst0__self_value_O),
    .value(Register_comb_inst0__value)
  );

  // Instancing generated Module: coreir.reg(width:4)
  wire  reg_P_inst0__clk;
  wire [3:0] reg_P_inst0__in;
  wire [3:0] reg_P_inst0__out;
  coreir_reg #(.clk_posedge(1),.init(4'h0),.width(4)) reg_P_inst0(
    .clk(reg_P_inst0__clk),
    .in(reg_P_inst0__in),
    .out(reg_P_inst0__out)
  );

  assign reg_P_inst0__in[3:0] = Register_comb_inst0__O0[3:0];

  assign O[3:0] = Register_comb_inst0__O1[3:0];

  assign Register_comb_inst0__en = en;

  assign Register_comb_inst0__self_value_O[3:0] = reg_P_inst0__out[3:0];

  assign Register_comb_inst0__value[3:0] = value[3:0];

  assign reg_P_inst0__clk = CLK;


endmodule  // Register

/* External Modules
module Mux2 (
  input  I0,
  input  I1,
  output  O,
  input  S
);

endmodule  // Mux2

*/
module RegisterMode_comb (
  output [3:0] O0,
  output  O1,
  output [3:0] O2,
  output [3:0] O3,
  input  clk_en,
  input [3:0] config_data,
  input  config_we,
  input [3:0] const_,
  input [1:0] mode,
  input [3:0] self_register_O,
  input [3:0] value
);


  wire  Mux2_inst0__I0;
  wire  Mux2_inst0__I1;
  wire  Mux2_inst0__O;
  wire  Mux2_inst0__S;
  Mux2 Mux2_inst0(
    .I0(Mux2_inst0__I0),
    .I1(Mux2_inst0__I1),
    .O(Mux2_inst0__O),
    .S(Mux2_inst0__S)
  );

  wire  Mux2_inst1__I0;
  wire  Mux2_inst1__I1;
  wire  Mux2_inst1__O;
  wire  Mux2_inst1__S;
  Mux2 Mux2_inst1(
    .I0(Mux2_inst1__I0),
    .I1(Mux2_inst1__I1),
    .O(Mux2_inst1__O),
    .S(Mux2_inst1__S)
  );

  wire  Mux2_inst2__I0;
  wire  Mux2_inst2__I1;
  wire  Mux2_inst2__O;
  wire  Mux2_inst2__S;
  Mux2 Mux2_inst2(
    .I0(Mux2_inst2__I0),
    .I1(Mux2_inst2__I1),
    .O(Mux2_inst2__O),
    .S(Mux2_inst2__S)
  );

  wire  Mux2_inst3__I0;
  wire  Mux2_inst3__I1;
  wire  Mux2_inst3__O;
  wire  Mux2_inst3__S;
  Mux2 Mux2_inst3(
    .I0(Mux2_inst3__I0),
    .I1(Mux2_inst3__I1),
    .O(Mux2_inst3__O),
    .S(Mux2_inst3__S)
  );

  wire  Mux2_inst4__I0;
  wire  Mux2_inst4__I1;
  wire  Mux2_inst4__O;
  wire  Mux2_inst4__S;
  Mux2 Mux2_inst4(
    .I0(Mux2_inst4__I0),
    .I1(Mux2_inst4__I1),
    .O(Mux2_inst4__O),
    .S(Mux2_inst4__S)
  );

  wire  Mux2_inst5__I0;
  wire  Mux2_inst5__I1;
  wire  Mux2_inst5__O;
  wire  Mux2_inst5__S;
  Mux2 Mux2_inst5(
    .I0(Mux2_inst5__I0),
    .I1(Mux2_inst5__I1),
    .O(Mux2_inst5__O),
    .S(Mux2_inst5__S)
  );

  wire [3:0] Mux2_x4_inst0__I0;
  wire [3:0] Mux2_x4_inst0__I1;
  wire [3:0] Mux2_x4_inst0__O;
  wire  Mux2_x4_inst0__S;
  Mux2_x4 Mux2_x4_inst0(
    .I0(Mux2_x4_inst0__I0),
    .I1(Mux2_x4_inst0__I1),
    .O(Mux2_x4_inst0__O),
    .S(Mux2_x4_inst0__S)
  );

  wire [3:0] Mux2_x4_inst1__I0;
  wire [3:0] Mux2_x4_inst1__I1;
  wire [3:0] Mux2_x4_inst1__O;
  wire  Mux2_x4_inst1__S;
  Mux2_x4 Mux2_x4_inst1(
    .I0(Mux2_x4_inst1__I0),
    .I1(Mux2_x4_inst1__I1),
    .O(Mux2_x4_inst1__O),
    .S(Mux2_x4_inst1__S)
  );

  wire [3:0] Mux2_x4_inst10__I0;
  wire [3:0] Mux2_x4_inst10__I1;
  wire [3:0] Mux2_x4_inst10__O;
  wire  Mux2_x4_inst10__S;
  Mux2_x4 Mux2_x4_inst10(
    .I0(Mux2_x4_inst10__I0),
    .I1(Mux2_x4_inst10__I1),
    .O(Mux2_x4_inst10__O),
    .S(Mux2_x4_inst10__S)
  );

  wire [3:0] Mux2_x4_inst11__I0;
  wire [3:0] Mux2_x4_inst11__I1;
  wire [3:0] Mux2_x4_inst11__O;
  wire  Mux2_x4_inst11__S;
  Mux2_x4 Mux2_x4_inst11(
    .I0(Mux2_x4_inst11__I0),
    .I1(Mux2_x4_inst11__I1),
    .O(Mux2_x4_inst11__O),
    .S(Mux2_x4_inst11__S)
  );

  wire [3:0] Mux2_x4_inst12__I0;
  wire [3:0] Mux2_x4_inst12__I1;
  wire [3:0] Mux2_x4_inst12__O;
  wire  Mux2_x4_inst12__S;
  Mux2_x4 Mux2_x4_inst12(
    .I0(Mux2_x4_inst12__I0),
    .I1(Mux2_x4_inst12__I1),
    .O(Mux2_x4_inst12__O),
    .S(Mux2_x4_inst12__S)
  );

  wire [3:0] Mux2_x4_inst13__I0;
  wire [3:0] Mux2_x4_inst13__I1;
  wire [3:0] Mux2_x4_inst13__O;
  wire  Mux2_x4_inst13__S;
  Mux2_x4 Mux2_x4_inst13(
    .I0(Mux2_x4_inst13__I0),
    .I1(Mux2_x4_inst13__I1),
    .O(Mux2_x4_inst13__O),
    .S(Mux2_x4_inst13__S)
  );

  wire [3:0] Mux2_x4_inst14__I0;
  wire [3:0] Mux2_x4_inst14__I1;
  wire [3:0] Mux2_x4_inst14__O;
  wire  Mux2_x4_inst14__S;
  Mux2_x4 Mux2_x4_inst14(
    .I0(Mux2_x4_inst14__I0),
    .I1(Mux2_x4_inst14__I1),
    .O(Mux2_x4_inst14__O),
    .S(Mux2_x4_inst14__S)
  );

  wire [3:0] Mux2_x4_inst2__I0;
  wire [3:0] Mux2_x4_inst2__I1;
  wire [3:0] Mux2_x4_inst2__O;
  wire  Mux2_x4_inst2__S;
  Mux2_x4 Mux2_x4_inst2(
    .I0(Mux2_x4_inst2__I0),
    .I1(Mux2_x4_inst2__I1),
    .O(Mux2_x4_inst2__O),
    .S(Mux2_x4_inst2__S)
  );

  wire [3:0] Mux2_x4_inst3__I0;
  wire [3:0] Mux2_x4_inst3__I1;
  wire [3:0] Mux2_x4_inst3__O;
  wire  Mux2_x4_inst3__S;
  Mux2_x4 Mux2_x4_inst3(
    .I0(Mux2_x4_inst3__I0),
    .I1(Mux2_x4_inst3__I1),
    .O(Mux2_x4_inst3__O),
    .S(Mux2_x4_inst3__S)
  );

  wire [3:0] Mux2_x4_inst4__I0;
  wire [3:0] Mux2_x4_inst4__I1;
  wire [3:0] Mux2_x4_inst4__O;
  wire  Mux2_x4_inst4__S;
  Mux2_x4 Mux2_x4_inst4(
    .I0(Mux2_x4_inst4__I0),
    .I1(Mux2_x4_inst4__I1),
    .O(Mux2_x4_inst4__O),
    .S(Mux2_x4_inst4__S)
  );

  wire [3:0] Mux2_x4_inst5__I0;
  wire [3:0] Mux2_x4_inst5__I1;
  wire [3:0] Mux2_x4_inst5__O;
  wire  Mux2_x4_inst5__S;
  Mux2_x4 Mux2_x4_inst5(
    .I0(Mux2_x4_inst5__I0),
    .I1(Mux2_x4_inst5__I1),
    .O(Mux2_x4_inst5__O),
    .S(Mux2_x4_inst5__S)
  );

  wire [3:0] Mux2_x4_inst6__I0;
  wire [3:0] Mux2_x4_inst6__I1;
  wire [3:0] Mux2_x4_inst6__O;
  wire  Mux2_x4_inst6__S;
  Mux2_x4 Mux2_x4_inst6(
    .I0(Mux2_x4_inst6__I0),
    .I1(Mux2_x4_inst6__I1),
    .O(Mux2_x4_inst6__O),
    .S(Mux2_x4_inst6__S)
  );

  wire [3:0] Mux2_x4_inst7__I0;
  wire [3:0] Mux2_x4_inst7__I1;
  wire [3:0] Mux2_x4_inst7__O;
  wire  Mux2_x4_inst7__S;
  Mux2_x4 Mux2_x4_inst7(
    .I0(Mux2_x4_inst7__I0),
    .I1(Mux2_x4_inst7__I1),
    .O(Mux2_x4_inst7__O),
    .S(Mux2_x4_inst7__S)
  );

  wire [3:0] Mux2_x4_inst8__I0;
  wire [3:0] Mux2_x4_inst8__I1;
  wire [3:0] Mux2_x4_inst8__O;
  wire  Mux2_x4_inst8__S;
  Mux2_x4 Mux2_x4_inst8(
    .I0(Mux2_x4_inst8__I0),
    .I1(Mux2_x4_inst8__I1),
    .O(Mux2_x4_inst8__O),
    .S(Mux2_x4_inst8__S)
  );

  wire [3:0] Mux2_x4_inst9__I0;
  wire [3:0] Mux2_x4_inst9__I1;
  wire [3:0] Mux2_x4_inst9__O;
  wire  Mux2_x4_inst9__S;
  Mux2_x4 Mux2_x4_inst9(
    .I0(Mux2_x4_inst9__I0),
    .I1(Mux2_x4_inst9__I1),
    .O(Mux2_x4_inst9__O),
    .S(Mux2_x4_inst9__S)
  );

  wire  bit_const_0_None__out;
  corebit_const #(.value(0)) bit_const_0_None(
    .out(bit_const_0_None__out)
  );

  wire  bit_const_1_None__out;
  corebit_const #(.value(1)) bit_const_1_None(
    .out(bit_const_1_None__out)
  );

  // Instancing generated Module: coreir.const(width:2)
  wire [1:0] const_0_2__out;
  coreir_const #(.value(2'h0),.width(2)) const_0_2(
    .out(const_0_2__out)
  );

  // Instancing generated Module: coreir.const(width:2)
  wire [1:0] const_1_2__out;
  coreir_const #(.value(2'h1),.width(2)) const_1_2(
    .out(const_1_2__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst0__in0;
  wire [1:0] eq_inst0__in1;
  wire  eq_inst0__out;
  coreir_eq #(.width(2)) eq_inst0(
    .in0(eq_inst0__in0),
    .in1(eq_inst0__in1),
    .out(eq_inst0__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst1__in0;
  wire [1:0] eq_inst1__in1;
  wire  eq_inst1__out;
  coreir_eq #(.width(2)) eq_inst1(
    .in0(eq_inst1__in0),
    .in1(eq_inst1__in1),
    .out(eq_inst1__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst10__in0;
  wire [1:0] eq_inst10__in1;
  wire  eq_inst10__out;
  coreir_eq #(.width(2)) eq_inst10(
    .in0(eq_inst10__in0),
    .in1(eq_inst10__in1),
    .out(eq_inst10__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst11__in0;
  wire [1:0] eq_inst11__in1;
  wire  eq_inst11__out;
  coreir_eq #(.width(2)) eq_inst11(
    .in0(eq_inst11__in0),
    .in1(eq_inst11__in1),
    .out(eq_inst11__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst12__in0;
  wire [1:0] eq_inst12__in1;
  wire  eq_inst12__out;
  coreir_eq #(.width(2)) eq_inst12(
    .in0(eq_inst12__in0),
    .in1(eq_inst12__in1),
    .out(eq_inst12__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst13__in0;
  wire [1:0] eq_inst13__in1;
  wire  eq_inst13__out;
  coreir_eq #(.width(2)) eq_inst13(
    .in0(eq_inst13__in0),
    .in1(eq_inst13__in1),
    .out(eq_inst13__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst14__in0;
  wire [1:0] eq_inst14__in1;
  wire  eq_inst14__out;
  coreir_eq #(.width(2)) eq_inst14(
    .in0(eq_inst14__in0),
    .in1(eq_inst14__in1),
    .out(eq_inst14__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst15__in0;
  wire [1:0] eq_inst15__in1;
  wire  eq_inst15__out;
  coreir_eq #(.width(2)) eq_inst15(
    .in0(eq_inst15__in0),
    .in1(eq_inst15__in1),
    .out(eq_inst15__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst16__in0;
  wire [1:0] eq_inst16__in1;
  wire  eq_inst16__out;
  coreir_eq #(.width(2)) eq_inst16(
    .in0(eq_inst16__in0),
    .in1(eq_inst16__in1),
    .out(eq_inst16__out)
  );

  wire  eq_inst17__in0;
  wire  eq_inst17__in1;
  wire  eq_inst17__out;
  corebit_and eq_inst17(
    .in0(eq_inst17__in0),
    .in1(eq_inst17__in1),
    .out(eq_inst17__out)
  );

  wire  eq_inst18__in0;
  wire  eq_inst18__in1;
  wire  eq_inst18__out;
  corebit_and eq_inst18(
    .in0(eq_inst18__in0),
    .in1(eq_inst18__in1),
    .out(eq_inst18__out)
  );

  wire  eq_inst19__in0;
  wire  eq_inst19__in1;
  wire  eq_inst19__out;
  corebit_and eq_inst19(
    .in0(eq_inst19__in0),
    .in1(eq_inst19__in1),
    .out(eq_inst19__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst2__in0;
  wire [1:0] eq_inst2__in1;
  wire  eq_inst2__out;
  coreir_eq #(.width(2)) eq_inst2(
    .in0(eq_inst2__in0),
    .in1(eq_inst2__in1),
    .out(eq_inst2__out)
  );

  wire  eq_inst20__in0;
  wire  eq_inst20__in1;
  wire  eq_inst20__out;
  corebit_and eq_inst20(
    .in0(eq_inst20__in0),
    .in1(eq_inst20__in1),
    .out(eq_inst20__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst3__in0;
  wire [1:0] eq_inst3__in1;
  wire  eq_inst3__out;
  coreir_eq #(.width(2)) eq_inst3(
    .in0(eq_inst3__in0),
    .in1(eq_inst3__in1),
    .out(eq_inst3__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst4__in0;
  wire [1:0] eq_inst4__in1;
  wire  eq_inst4__out;
  coreir_eq #(.width(2)) eq_inst4(
    .in0(eq_inst4__in0),
    .in1(eq_inst4__in1),
    .out(eq_inst4__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst5__in0;
  wire [1:0] eq_inst5__in1;
  wire  eq_inst5__out;
  coreir_eq #(.width(2)) eq_inst5(
    .in0(eq_inst5__in0),
    .in1(eq_inst5__in1),
    .out(eq_inst5__out)
  );

  wire  eq_inst6__in0;
  wire  eq_inst6__in1;
  wire  eq_inst6__out;
  corebit_and eq_inst6(
    .in0(eq_inst6__in0),
    .in1(eq_inst6__in1),
    .out(eq_inst6__out)
  );

  wire  eq_inst7__in0;
  wire  eq_inst7__in1;
  wire  eq_inst7__out;
  corebit_and eq_inst7(
    .in0(eq_inst7__in0),
    .in1(eq_inst7__in1),
    .out(eq_inst7__out)
  );

  wire  eq_inst8__in0;
  wire  eq_inst8__in1;
  wire  eq_inst8__out;
  corebit_and eq_inst8(
    .in0(eq_inst8__in0),
    .in1(eq_inst8__in1),
    .out(eq_inst8__out)
  );

  // Instancing generated Module: coreir.eq(width:2)
  wire [1:0] eq_inst9__in0;
  wire [1:0] eq_inst9__in1;
  wire  eq_inst9__out;
  coreir_eq #(.width(2)) eq_inst9(
    .in0(eq_inst9__in0),
    .in1(eq_inst9__in1),
    .out(eq_inst9__out)
  );

  assign Mux2_inst0__I0 = clk_en;

  assign Mux2_inst0__I1 = bit_const_0_None__out;

  assign Mux2_inst1__I0 = Mux2_inst0__O;

  assign Mux2_inst0__S = eq_inst1__out;

  assign Mux2_inst1__I1 = bit_const_0_None__out;

  assign Mux2_inst2__I0 = Mux2_inst1__O;

  assign Mux2_inst1__S = eq_inst4__out;

  assign Mux2_inst2__I1 = bit_const_1_None__out;

  assign Mux2_inst2__S = eq_inst7__out;

  assign Mux2_inst3__I0 = clk_en;

  assign Mux2_inst3__I1 = bit_const_0_None__out;

  assign Mux2_inst4__I0 = Mux2_inst3__O;

  assign Mux2_inst3__S = eq_inst10__out;

  assign Mux2_inst4__I1 = bit_const_0_None__out;

  assign Mux2_inst5__I0 = Mux2_inst4__O;

  assign Mux2_inst4__S = eq_inst14__out;

  assign Mux2_inst5__I1 = bit_const_1_None__out;

  assign O1 = Mux2_inst5__O;

  assign Mux2_inst5__S = eq_inst18__out;

  assign Mux2_x4_inst0__I0[3:0] = value[3:0];

  assign Mux2_x4_inst0__I1[3:0] = value[3:0];

  assign Mux2_x4_inst2__I0[3:0] = Mux2_x4_inst0__O[3:0];

  assign Mux2_x4_inst0__S = eq_inst0__out;

  assign Mux2_x4_inst1__I0[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst1__I1[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst3__I0[3:0] = Mux2_x4_inst1__O[3:0];

  assign Mux2_x4_inst1__S = eq_inst2__out;

  assign Mux2_x4_inst10__I0[3:0] = Mux2_x4_inst7__O[3:0];

  assign Mux2_x4_inst10__I1[3:0] = const_[3:0];

  assign Mux2_x4_inst13__I0[3:0] = Mux2_x4_inst10__O[3:0];

  assign Mux2_x4_inst10__S = eq_inst15__out;

  assign Mux2_x4_inst11__I0[3:0] = Mux2_x4_inst8__O[3:0];

  assign Mux2_x4_inst11__I1[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst14__I0[3:0] = Mux2_x4_inst11__O[3:0];

  assign Mux2_x4_inst11__S = eq_inst16__out;

  assign Mux2_x4_inst12__I0[3:0] = Mux2_x4_inst9__O[3:0];

  assign Mux2_x4_inst12__I1[3:0] = config_data[3:0];

  assign O0[3:0] = Mux2_x4_inst12__O[3:0];

  assign Mux2_x4_inst12__S = eq_inst17__out;

  assign Mux2_x4_inst13__I1[3:0] = self_register_O[3:0];

  assign O2[3:0] = Mux2_x4_inst13__O[3:0];

  assign Mux2_x4_inst13__S = eq_inst19__out;

  assign Mux2_x4_inst14__I1[3:0] = self_register_O[3:0];

  assign O3[3:0] = Mux2_x4_inst14__O[3:0];

  assign Mux2_x4_inst14__S = eq_inst20__out;

  assign Mux2_x4_inst2__I1[3:0] = value[3:0];

  assign Mux2_x4_inst4__I0[3:0] = Mux2_x4_inst2__O[3:0];

  assign Mux2_x4_inst2__S = eq_inst3__out;

  assign Mux2_x4_inst3__I1[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst5__I0[3:0] = Mux2_x4_inst3__O[3:0];

  assign Mux2_x4_inst3__S = eq_inst5__out;

  assign Mux2_x4_inst4__I1[3:0] = config_data[3:0];

  assign Mux2_x4_inst4__S = eq_inst6__out;

  assign Mux2_x4_inst5__I1[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst5__S = eq_inst8__out;

  assign Mux2_x4_inst6__I0[3:0] = value[3:0];

  assign Mux2_x4_inst6__I1[3:0] = value[3:0];

  assign Mux2_x4_inst9__I0[3:0] = Mux2_x4_inst6__O[3:0];

  assign Mux2_x4_inst6__S = eq_inst9__out;

  assign Mux2_x4_inst7__I0[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst7__I1[3:0] = value[3:0];

  assign Mux2_x4_inst7__S = eq_inst11__out;

  assign Mux2_x4_inst8__I0[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst8__I1[3:0] = self_register_O[3:0];

  assign Mux2_x4_inst8__S = eq_inst12__out;

  assign Mux2_x4_inst9__I1[3:0] = value[3:0];

  assign Mux2_x4_inst9__S = eq_inst13__out;

  assign eq_inst17__in1 = bit_const_1_None__out;

  assign eq_inst18__in1 = bit_const_1_None__out;

  assign eq_inst19__in1 = bit_const_1_None__out;

  assign eq_inst20__in1 = bit_const_1_None__out;

  assign eq_inst6__in1 = bit_const_1_None__out;

  assign eq_inst7__in1 = bit_const_1_None__out;

  assign eq_inst8__in1 = bit_const_1_None__out;

  assign eq_inst13__in1[1:0] = const_0_2__out[1:0];

  assign eq_inst14__in1[1:0] = const_0_2__out[1:0];

  assign eq_inst15__in1[1:0] = const_0_2__out[1:0];

  assign eq_inst16__in1[1:0] = const_0_2__out[1:0];

  assign eq_inst3__in1[1:0] = const_0_2__out[1:0];

  assign eq_inst4__in1[1:0] = const_0_2__out[1:0];

  assign eq_inst5__in1[1:0] = const_0_2__out[1:0];

  assign eq_inst0__in1[1:0] = const_1_2__out[1:0];

  assign eq_inst1__in1[1:0] = const_1_2__out[1:0];

  assign eq_inst10__in1[1:0] = const_1_2__out[1:0];

  assign eq_inst11__in1[1:0] = const_1_2__out[1:0];

  assign eq_inst12__in1[1:0] = const_1_2__out[1:0];

  assign eq_inst2__in1[1:0] = const_1_2__out[1:0];

  assign eq_inst9__in1[1:0] = const_1_2__out[1:0];

  assign eq_inst0__in0[1:0] = mode[1:0];

  assign eq_inst1__in0[1:0] = mode[1:0];

  assign eq_inst10__in0[1:0] = mode[1:0];

  assign eq_inst11__in0[1:0] = mode[1:0];

  assign eq_inst12__in0[1:0] = mode[1:0];

  assign eq_inst13__in0[1:0] = mode[1:0];

  assign eq_inst14__in0[1:0] = mode[1:0];

  assign eq_inst15__in0[1:0] = mode[1:0];

  assign eq_inst16__in0[1:0] = mode[1:0];

  assign eq_inst17__in0 = config_we;

  assign eq_inst18__in0 = config_we;

  assign eq_inst19__in0 = config_we;

  assign eq_inst2__in0[1:0] = mode[1:0];

  assign eq_inst20__in0 = config_we;

  assign eq_inst3__in0[1:0] = mode[1:0];

  assign eq_inst4__in0[1:0] = mode[1:0];

  assign eq_inst5__in0[1:0] = mode[1:0];

  assign eq_inst6__in0 = config_we;

  assign eq_inst7__in0 = config_we;

  assign eq_inst8__in0 = config_we;

  assign eq_inst9__in0[1:0] = mode[1:0];


endmodule  // RegisterMode_comb

module RegisterMode (
  input  CLK,
  output [3:0] O0,
  output [3:0] O1,
  input  clk_en,
  input [3:0] config_data,
  input  config_we,
  input [3:0] const_,
  input [1:0] mode,
  input [3:0] value
);


  wire [3:0] RegisterMode_comb_inst0__O0;
  wire  RegisterMode_comb_inst0__O1;
  wire [3:0] RegisterMode_comb_inst0__O2;
  wire [3:0] RegisterMode_comb_inst0__O3;
  wire  RegisterMode_comb_inst0__clk_en;
  wire [3:0] RegisterMode_comb_inst0__config_data;
  wire  RegisterMode_comb_inst0__config_we;
  wire [3:0] RegisterMode_comb_inst0__const_;
  wire [1:0] RegisterMode_comb_inst0__mode;
  wire [3:0] RegisterMode_comb_inst0__self_register_O;
  wire [3:0] RegisterMode_comb_inst0__value;
  RegisterMode_comb RegisterMode_comb_inst0(
    .O0(RegisterMode_comb_inst0__O0),
    .O1(RegisterMode_comb_inst0__O1),
    .O2(RegisterMode_comb_inst0__O2),
    .O3(RegisterMode_comb_inst0__O3),
    .clk_en(RegisterMode_comb_inst0__clk_en),
    .config_data(RegisterMode_comb_inst0__config_data),
    .config_we(RegisterMode_comb_inst0__config_we),
    .const_(RegisterMode_comb_inst0__const_),
    .mode(RegisterMode_comb_inst0__mode),
    .self_register_O(RegisterMode_comb_inst0__self_register_O),
    .value(RegisterMode_comb_inst0__value)
  );

  wire  Register_inst0__CLK;
  wire [3:0] Register_inst0__O;
  wire  Register_inst0__en;
  wire [3:0] Register_inst0__value;
  Register Register_inst0(
    .CLK(Register_inst0__CLK),
    .O(Register_inst0__O),
    .en(Register_inst0__en),
    .value(Register_inst0__value)
  );

  assign Register_inst0__value[3:0] = RegisterMode_comb_inst0__O0[3:0];

  assign Register_inst0__en = RegisterMode_comb_inst0__O1;

  assign O0[3:0] = RegisterMode_comb_inst0__O2[3:0];

  assign O1[3:0] = RegisterMode_comb_inst0__O3[3:0];

  assign RegisterMode_comb_inst0__clk_en = clk_en;

  assign RegisterMode_comb_inst0__config_data[3:0] = config_data[3:0];

  assign RegisterMode_comb_inst0__config_we = config_we;

  assign RegisterMode_comb_inst0__const_[3:0] = const_[3:0];

  assign RegisterMode_comb_inst0__mode[1:0] = mode[1:0];

  assign RegisterMode_comb_inst0__self_register_O[3:0] = Register_inst0__O[3:0];

  assign RegisterMode_comb_inst0__value[3:0] = value[3:0];

  assign Register_inst0__CLK = CLK;


endmodule  // RegisterMode


module coreir_mux #(parameter width=1) (
  input [width-1:0] in0,
  input [width-1:0] in1,
  input sel,
  output [width-1:0] out
);
  assign out = sel ? in1 : in0;

endmodule  // coreir_mux

module corebit_const #(parameter value=1) (
  output out
);
  assign out = value;

endmodule  // corebit_const

module eq (
  input  I0,
  input  I1,
  output  O
);


  wire  bit_const_0_None__out;
  corebit_const #(.value(0)) bit_const_0_None(
    .out(bit_const_0_None__out)
  );

  assign O = bit_const_0_None__out;


endmodule  // eq

// Generated from commonlib.muxn(N:2, width:1)
module commonlib_muxn__N2__width1 (
  input [0:0] in_data_0,
  input [0:0] in_data_1,
  input [0:0] in_sel,
  output [0:0] out
);


  // Instancing generated Module: coreir.mux(width:1)
  wire [0:0] _join__in0;
  wire [0:0] _join__in1;
  wire [0:0] _join__out;
  wire  _join__sel;
  coreir_mux #(.width(1)) _join(
    .in0(_join__in0),
    .in1(_join__in1),
    .out(_join__out),
    .sel(_join__sel)
  );

  assign _join__in0[0:0] = in_data_0[0:0];

  assign _join__in1[0:0] = in_data_1[0:0];

  assign out[0:0] = _join__out[0:0];

  assign _join__sel = in_sel[0];


endmodule  // commonlib_muxn__N2__width1

module Mux2xOutBit (
  input  I0,
  input  I1,
  output  O,
  input  S
);


  // Instancing generated Module: commonlib.muxn(N:2, width:1)
  wire [0:0] coreir_commonlib_mux2x1_inst0__in_data_0;
  wire [0:0] coreir_commonlib_mux2x1_inst0__in_data_1;
  wire [0:0] coreir_commonlib_mux2x1_inst0__in_sel;
  wire [0:0] coreir_commonlib_mux2x1_inst0__out;
  commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0(
    .in_data_0(coreir_commonlib_mux2x1_inst0__in_data_0),
    .in_data_1(coreir_commonlib_mux2x1_inst0__in_data_1),
    .in_sel(coreir_commonlib_mux2x1_inst0__in_sel),
    .out(coreir_commonlib_mux2x1_inst0__out)
  );

  assign coreir_commonlib_mux2x1_inst0__in_data_0[0] = I0;

  assign coreir_commonlib_mux2x1_inst0__in_data_1[0] = I1;

  assign coreir_commonlib_mux2x1_inst0__in_sel[0] = S;

  assign O = coreir_commonlib_mux2x1_inst0__out[0];


endmodule  // Mux2xOutBit

module logic (
  output  O0,
  input  a_0
);


  wire  Mux2xOutBit_inst0__I0;
  wire  Mux2xOutBit_inst0__I1;
  wire  Mux2xOutBit_inst0__O;
  wire  Mux2xOutBit_inst0__S;
  Mux2xOutBit Mux2xOutBit_inst0(
    .I0(Mux2xOutBit_inst0__I0),
    .I1(Mux2xOutBit_inst0__I1),
    .O(Mux2xOutBit_inst0__O),
    .S(Mux2xOutBit_inst0__S)
  );

  wire  bit_const_0_None__out;
  corebit_const #(.value(0)) bit_const_0_None(
    .out(bit_const_0_None__out)
  );

  wire  bit_const_1_None__out;
  corebit_const #(.value(1)) bit_const_1_None(
    .out(bit_const_1_None__out)
  );

  wire  eq_inst0__I0;
  wire  eq_inst0__I1;
  wire  eq_inst0__O;
  eq eq_inst0(
    .I0(eq_inst0__I0),
    .I1(eq_inst0__I1),
    .O(eq_inst0__O)
  );

  assign Mux2xOutBit_inst0__I0 = bit_const_1_None__out;

  assign Mux2xOutBit_inst0__I1 = bit_const_0_None__out;

  assign O0 = Mux2xOutBit_inst0__O;

  assign Mux2xOutBit_inst0__S = eq_inst0__O;

  assign eq_inst0__I1 = bit_const_0_None__out;

  assign eq_inst0__I0 = a_0;


endmodule  // logic

module Foo (
  input  a,
  output  c
);


  wire  logic_inst0__O0;
  wire  logic_inst0__a_0;
  logic logic_inst0(
    .O0(logic_inst0__O0),
    .a_0(logic_inst0__a_0)
  );

  assign c = logic_inst0__O0;

  assign logic_inst0__a_0 = a;


endmodule  // Foo


module corebit_not (
  input in,
  output out
);
  assign out = ~in;

endmodule  // corebit_not

/* External Modules
module Mux2 (
  input  I0,
  input  I1,
  output  O,
  input  S
);

endmodule  // Mux2

*/
module if_statement_nested (
  input [3:0] I,
  output  O,
  input [1:0] S
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

  wire  not_inst0__in;
  wire  not_inst0__out;
  corebit_not not_inst0(
    .in(not_inst0__in),
    .out(not_inst0__out)
  );

  assign Mux2_inst0__I0 = I[1];

  assign Mux2_inst0__I1 = I[0];

  assign Mux2_inst1__I1 = Mux2_inst0__O;

  assign Mux2_inst0__S = S[1];

  assign Mux2_inst1__I0 = I[2];

  assign Mux2_inst2__I1 = Mux2_inst1__O;

  assign Mux2_inst1__S = not_inst0__out;

  assign Mux2_inst2__I0 = I[3];

  assign O = Mux2_inst2__O;

  assign Mux2_inst2__S = S[1];

  assign not_inst0__in = S[1];


endmodule  // if_statement_nested


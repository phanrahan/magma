/* External Modules
module or (
  input  I0,
  input  I1,
  output  O
);

endmodule  // or

*/
/* External Modules
module invert (
  input  I,
  output  O
);

endmodule  // invert

*/
/* External Modules
module and (
  input  I0,
  input  I1,
  output  O
);

endmodule  // and

*/
module Test (
  input  I0,
  input  I1,
  output  O,
  input  S
);


  wire  and_inst0__I0;
  wire  and_inst0__I1;
  wire  and_inst0__O;
  and and_inst0(
    .I0(and_inst0__I0),
    .I1(and_inst0__I1),
    .O(and_inst0__O)
  );

  wire  and_inst1__I0;
  wire  and_inst1__I1;
  wire  and_inst1__O;
  and and_inst1(
    .I0(and_inst1__I0),
    .I1(and_inst1__I1),
    .O(and_inst1__O)
  );

  wire  invert_inst0__I;
  wire  invert_inst0__O;
  invert invert_inst0(
    .I(invert_inst0__I),
    .O(invert_inst0__O)
  );

  wire  or_inst0__I0;
  wire  or_inst0__I1;
  wire  or_inst0__O;
  or or_inst0(
    .I0(or_inst0__I0),
    .I1(or_inst0__I1),
    .O(or_inst0__O)
  );

  assign and_inst0__I0 = S;

  assign and_inst0__I1 = I1;

  assign or_inst0__I0 = and_inst0__O;

  assign and_inst1__I0 = invert_inst0__O;

  assign and_inst1__I1 = I0;

  assign or_inst0__I1 = and_inst1__O;

  assign invert_inst0__I = S;

  assign O = or_inst0__O;


endmodule  // Test


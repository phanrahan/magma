/* External Modules
module And2 (
  input  I0,
  input  I1,
  output  O
);

endmodule  // And2

*/
module main (
  input [1:0] I,
  output  O
);


  wire  And2_inst0__I0;
  wire  And2_inst0__I1;
  wire  And2_inst0__O;
  And2 And2_inst0(
    .I0(And2_inst0__I0),
    .I1(And2_inst0__I1),
    .O(And2_inst0__O)
  );

  assign And2_inst0__I0 = I[0];

  assign And2_inst0__I1 = I[1];

  assign O = And2_inst0__O;


endmodule  // main


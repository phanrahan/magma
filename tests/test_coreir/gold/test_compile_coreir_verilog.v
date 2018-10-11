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


  wire  inst0__I0;
  wire  inst0__I1;
  wire  inst0__O;
  And2 inst0(
    .I0(inst0__I0),
    .I1(inst0__I1),
    .O(inst0__O)
  );

  assign inst0__I0 = I[0];

  assign inst0__I1 = I[1];

  assign O = inst0__O;


endmodule  // main


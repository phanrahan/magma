//Module: And2 defined externally


module main (
  input [1:0] I,
  output  O
);
  //Wire declarations for instance 'inst0' (Module And2)
  wire  inst0__I0;
  wire  inst0__I1;
  wire  inst0__O;
  And2 inst0(
    .I0(inst0__I0),
    .I1(inst0__I1),
    .O(inst0__O)
  );

  //All the connections
  assign inst0__I0 = I[0];
  assign inst0__I1 = I[1];
  assign O = inst0__O;

endmodule //main

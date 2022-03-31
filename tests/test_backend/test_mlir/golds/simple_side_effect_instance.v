module no_outputs(	// <stdin>:1:1
  input I);

endmodule

module simple_side_effect_instance(	// <stdin>:5:1
  input  I,
  output O);

  no_outputs no_outputs_inst0 (	// <stdin>:6:5
    .I (I)
  );
  assign O = I;	// <stdin>:7:5
endmodule


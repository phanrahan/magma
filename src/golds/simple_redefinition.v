module simple_redefinition_module(
  input  a,
  output y);

  assign y = a;	// <stdin>:3:5
endmodule

module simple_redefinition(
  input  a,
  output y);

  wire simple_redefinition_module_inst0_y;	// <stdin>:6:43

  simple_redefinition_module simple_redefinition_module_inst0 (	// <stdin>:6:43
    .a (a),
    .y (simple_redefinition_module_inst0_y)
  );
  simple_redefinition_module simple_redefinition_module_inst1 (	// <stdin>:7:43
    .a (simple_redefinition_module_inst0_y),	// <stdin>:6:43
    .y (y)
  );
endmodule


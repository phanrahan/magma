module simple_redefinition_module(	// <stdin>:1:1
  input  a,
  output y);

  assign y = a;	// <stdin>:2:5
endmodule

module simple_redefinition(	// <stdin>:4:1
  input  a,
  output y);

  wire simple_redefinition_module_inst0_y;	// <stdin>:5:10

  simple_redefinition_module simple_redefinition_module_inst0 (	// <stdin>:5:10
    .a (a),
    .y (simple_redefinition_module_inst0_y)
  );
  simple_redefinition_module simple_redefinition_module_inst1 (	// <stdin>:6:10
    .a (simple_redefinition_module_inst0_y),	// <stdin>:5:10
    .y (y)
  );
endmodule


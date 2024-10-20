module simple_redefinition_module(
  input  a,
  output y
);

  assign y = a;
endmodule

module simple_redefinition(
  input  a,
  output y
);

  wire _simple_redefinition_module_inst0_y;
  simple_redefinition_module simple_redefinition_module_inst0 (
    .a (a),
    .y (_simple_redefinition_module_inst0_y)
  );
  simple_redefinition_module simple_redefinition_module_inst1 (
    .a (_simple_redefinition_module_inst0_y),
    .y (y)
  );
endmodule


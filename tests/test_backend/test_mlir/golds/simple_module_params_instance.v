module simple_module_params
  #(parameter /*integer*/ width,
    parameter /*integer*/ height) (
  input  I,
  output O
);

  assign O = I;
endmodule

module simple_module_params_instance(
  input  I,
  output O
);

  simple_module_params #(
    .width(10),
    .height(20)
  ) simple_module_params_inst0 (
    .I (I),
    .O (O)
  );
endmodule


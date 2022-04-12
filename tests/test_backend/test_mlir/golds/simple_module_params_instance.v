module simple_module_params
  #(parameter /*integer*/ width,
    parameter /*integer*/ height) (	// <stdin>:1:1
  input  I,
  output O);

  assign O = I;	// <stdin>:2:5
endmodule

module simple_module_params_instance(	// <stdin>:4:1
  input  I,
  output O);

  simple_module_params #(
    .width(10),
    .height(20)
  ) simple_module_params_inst0 (	// <stdin>:5:10
    .I (I),
    .O (O)
  );
endmodule


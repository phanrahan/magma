module coreir_const #(parameter value=1, parameter width=1) (
  output [width-1:0] out
);
  assign out = width'value;

endmodule  // coreir_const

module enum_test_max_value (
  input [2:0] I,
  output [2:0] O_0,
  output [2:0] O_1
);


  // Instancing generated Module: coreir.const(width:3)
  wire [2:0] const_4_3__out;
  coreir_const #(.value(3'h4),.width(3)) const_4_3(
    .out(const_4_3__out)
  );

  assign O_0[2:0] = I[2:0];

  assign O_1[2:0] = const_4_3__out[2:0];


endmodule  // enum_test_max_value


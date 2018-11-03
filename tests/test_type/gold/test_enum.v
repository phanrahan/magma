module coreir_const #(parameter value=1, parameter width=1) (
  output [width-1:0] out
);
  assign out = width'value;

endmodule  // coreir_const

module enum_test (
  input [1:0] I,
  output [1:0] O_0,
  output [1:0] O_1
);


  // Instancing generated Module: coreir.const(width:2)
  wire [1:0] const_0_2__out;
  coreir_const #(.value(2'h0),.width(2)) const_0_2(
    .out(const_0_2__out)
  );

  assign O_0[1:0] = I[1:0];

  assign O_1[1:0] = const_0_2__out[1:0];


endmodule  // enum_test


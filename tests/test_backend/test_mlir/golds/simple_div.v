module simple_div(
  input  [15:0] a,
                b,
  output [15:0] y,
                z
);

  assign y = a / b;
  assign z = $signed(a) / $signed(b);
endmodule


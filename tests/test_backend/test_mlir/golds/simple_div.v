// Generated by CIRCT circtorg-0.0.0-1713-g579d21b50
module simple_div(
  input  [15:0] a,
                b,
  output [15:0] y,
                z
);

  assign y = a / b;
  assign z = $signed(a) / $signed(b);
endmodule


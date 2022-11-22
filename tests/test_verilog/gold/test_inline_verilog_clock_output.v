module coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module corebit_term (
    input in
);

endmodule

module Foo (
    input x,
    input y
);

Foo bar (.x(x, .yy))

endmodule


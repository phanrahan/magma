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
    input y,
    input CLK,
    input RESET
);

assert property (@(posedge CLK) disable iff (! RESET) x |-> ##1 y);


assert property (@(posedge CLK) disable iff (! RESET) x |-> ##1 y);

endmodule


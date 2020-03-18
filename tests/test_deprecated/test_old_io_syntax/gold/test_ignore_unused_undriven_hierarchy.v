module corebit_undriven (
    output out
);

endmodule

module corebit_term (
    input in
);

endmodule

module Foo (
    input I0,
    input I1,
    output O0,
    output O1
);
corebit_term corebit_term_inst0 (
    .in(I1)
);
corebit_undriven corebit_undriven_inst0 (
    .out(O0)
);
assign O1 = I0;
endmodule

module Main (
    input I0,
    input I1,
    output O0,
    output O1
);
wire Foo_inst0_O1;
wire corebit_undriven_inst1_out;
Foo Foo_inst0 (
    .I0(I0),
    .I1(corebit_undriven_inst1_out),
    .O0(O0),
    .O1(Foo_inst0_O1)
);
corebit_term corebit_term_inst0 (
    .in(I1)
);
corebit_term corebit_term_inst1 (
    .in(Foo_inst0_O1)
);
corebit_undriven corebit_undriven_inst0 (
    .out(O1)
);
corebit_undriven corebit_undriven_inst1 (
    .out(corebit_undriven_inst1_out)
);
endmodule


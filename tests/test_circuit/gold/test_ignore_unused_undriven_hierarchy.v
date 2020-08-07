// Module `Bar` defined externally
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
wire Bar_inst0_I;
assign Bar_inst0_I = I1;
Bar Bar_inst0 (
    .I(Bar_inst0_I)
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
wire Foo_inst0_I0;
wire Foo_inst0_I1;
wire Foo_inst0_O1;
wire corebit_term_inst0_in;
wire corebit_term_inst1_in;
wire corebit_undriven_inst1_out;
assign Foo_inst0_I0 = I0;
assign Foo_inst0_I1 = corebit_undriven_inst1_out;
Foo Foo_inst0 (
    .I0(Foo_inst0_I0),
    .I1(Foo_inst0_I1),
    .O0(O0),
    .O1(Foo_inst0_O1)
);
assign corebit_term_inst0_in = I1;
corebit_term corebit_term_inst0 (
    .in(corebit_term_inst0_in)
);
assign corebit_term_inst1_in = Foo_inst0_O1;
corebit_term corebit_term_inst1 (
    .in(corebit_term_inst1_in)
);
corebit_undriven corebit_undriven_inst0 (
    .out(O1)
);
corebit_undriven corebit_undriven_inst1 (
    .out(corebit_undriven_inst1_out)
);
endmodule


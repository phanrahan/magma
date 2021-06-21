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
Bar Bar_inst0 (
    .I(I1)
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
    output O1,
    output O2__0,
    output O2__1,
    output [1:0] O3
);
wire Foo_inst0_O1;
wire corebit_undriven_inst2_out;
wire corebit_undriven_inst3_out;
Foo Foo_inst0 (
    .I0(I0),
    .I1(corebit_undriven_inst3_out),
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
    .out(O2__1)
);
corebit_undriven corebit_undriven_inst2 (
    .out(corebit_undriven_inst2_out)
);
corebit_undriven corebit_undriven_inst3 (
    .out(corebit_undriven_inst3_out)
);
assign O2__0 = 1'b1;
assign O3 = {corebit_undriven_inst2_out,1'b1};
endmodule


module corebit_term (
    input in
);

endmodule

module Foo_unq1 (
    input I
);
always @(*) $display("%x\n", I);
endmodule

module Foo (
    input I
);
always @(*) $display("%d\n", I);
endmodule

module Top (
    input I
);
Foo Foo_inst0 (
    .I(I)
);
Foo_unq1 Foo_inst1 (
    .I(I)
);
endmodule


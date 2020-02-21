// Module `Foo` defined externally
module Bar (
    input CLK,
    input ASYNCRESETN
);
Foo Foo_inst0 (
    .CLK(CLK),
    .ASYNCRESETN(ASYNCRESETN)
);
endmodule


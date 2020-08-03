// Module `Foo` defined externally
module Bar (
    input CLK,
    input ASYNCRESETN
);
wire Foo_inst0_CLK;
wire Foo_inst0_ASYNCRESETN;
assign Foo_inst0_CLK = CLK;
assign Foo_inst0_ASYNCRESETN = ASYNCRESETN;
Foo Foo_inst0 (
    .CLK(Foo_inst0_CLK),
    .ASYNCRESETN(Foo_inst0_ASYNCRESETN)
);
endmodule


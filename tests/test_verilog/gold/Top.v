// Module `FF` defined externally
module Top (
    input I,
    output O,
    input CLK
);
wire FF_inst0_I;
wire FF_inst0_O;
wire FF_inst0_CLK;
wire FF_inst1_I;
wire FF_inst1_O;
wire FF_inst1_CLK;
assign FF_inst0_I = I;
assign FF_inst0_CLK = CLK;
FF #(
    .init(0)
) FF_inst0 (
    .I(FF_inst0_I),
    .O(FF_inst0_O),
    .CLK(FF_inst0_CLK)
);
assign FF_inst1_I = FF_inst0_O;
assign FF_inst1_CLK = CLK;
FF #(
    .init(1)
) FF_inst1 (
    .I(FF_inst1_I),
    .O(FF_inst1_O),
    .CLK(FF_inst1_CLK)
);
assign O = FF_inst1_O;
endmodule


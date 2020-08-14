// Module `FF` defined externally
module Top (
    input I,
    output O,
    input CLK
);
wire FF_inst0_O;
wire FF_inst1_O;
FF #(
    .init(0)
) FF_inst0 (
    .I(I),
    .O(FF_inst0_O),
    .CLK(CLK)
);
FF #(
    .init(1)
) FF_inst1 (
    .I(FF_inst0_O),
    .O(FF_inst1_O),
    .CLK(CLK)
);
assign O = FF_inst1_O;
endmodule


// Module `FF` defined externally
module Top (
    input I,
    output O,
    input CLK
);
wire ff0_O;
wire ff1_O;
FF #(
    .init(0)
) ff0 (
    .I(I),
    .O(ff0_O),
    .CLK(CLK)
);
FF #(
    .init(1)
) ff1 (
    .I(ff0_O),
    .O(ff1_O),
    .CLK(CLK)
);
assign O = ff1_O;
endmodule


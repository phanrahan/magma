module FF(input I, output reg O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
module Main (
    input I,
    output O,
    input CLK
);
wire FF_inst0_O;
FF FF_inst0 (
    .I(I),
    .O(FF_inst0_O),
    .CLK(CLK)
);
assign O = FF_inst0_O;
endmodule


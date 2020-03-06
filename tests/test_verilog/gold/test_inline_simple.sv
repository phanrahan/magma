module _InlineVerilog (
    input O,
    input I
);

assert property (@(posedge CLK) I |-> ##1 O);

endmodule

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
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK)
);
_InlineVerilog _InlineVerilog_inst0 (
    .O(O),
    .I(I)
);
endmodule


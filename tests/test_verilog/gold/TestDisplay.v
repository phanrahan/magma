module corebit_term (
    input in
);

endmodule

module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
module TestDisplay (
    input I,
    output O,
    input CLK,
    input CE
);
wire _magma_inline_wire0;
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK),
    .CE(CE)
);
assign _magma_inline_wire0 = O;
corebit_term corebit_term_inst0 (
    .in(_magma_inline_wire0)
);
always @(posedge CLK) begin
    if (CE) $display("%0t: ff.O=%d, ff.I=%d", $time, _magma_inline_wire0, I);
end

endmodule


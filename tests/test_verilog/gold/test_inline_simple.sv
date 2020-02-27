module corebit_term (
    input in
);

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
corebit_term corebit_term_inst0 (
    .in(I)
);

assert property (@(posedge CLK) I |-> ##1 O);

endmodule


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
    input [1:0] arr,
    input CLK
);
wire _magma_inline_wire0;
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK)
);

assert property (@(posedge CLK) I |-> ##1 _magma_inline_wire0);


assert property (@(posedge CLK) arr[0] |-> ##1 arr[1]);

assign _magma_inline_wire0 = O;
endmodule


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
wire _foo_prefix_0;
wire _foo_prefix_1;
wire _magma_inline_wire2;
wire _magma_inline_wire3;
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK)
);
assign _foo_prefix_0 = O;
assign _foo_prefix_1 = I;
assign _magma_inline_wire2 = arr[0];
assign _magma_inline_wire3 = arr[1];

assert property (@(posedge CLK) _foo_prefix_1 |-> ##1 _foo_prefix_0);


assert property (@(posedge CLK) _magma_inline_wire2 |-> ##1 _magma_inline_wire3);

endmodule


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
wire FF_inst0_I;
wire FF_inst0_CLK;
wire _magma_inline_wire0;
assign FF_inst0_I = I;
assign FF_inst0_CLK = CLK;
FF FF_inst0 (
    .I(FF_inst0_I),
    .O(O),
    .CLK(FF_inst0_CLK)
);
assign _magma_inline_wire0 = O;

assert property (@(posedge CLK) I |-> ##1 _magma_inline_wire0);


assert property (@(posedge CLK) arr[0] |-> ##1 arr[1]);

endmodule


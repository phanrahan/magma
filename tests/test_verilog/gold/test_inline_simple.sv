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
wire O_magma_inline_wire;
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK)
);
assign O_magma_inline_wire = O;
corebit_term corebit_term_inst0 (
    .in(O_magma_inline_wire)
);

assert property (@(posedge CLK) I |-> ##1 O_magma_inline_wire);



assert property (@(posedge CLK) arr[0] |-> ##1 arr[1]);

endmodule


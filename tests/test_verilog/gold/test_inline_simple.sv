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
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK)
);
corebit_term corebit_term_inst0 (
    .in(arr[0])
);
corebit_term corebit_term_inst1 (
    .in(arr[1])
);

assert property (@(posedge CLK) I |-> ##1 O);



assert property (@(posedge CLK) arr[0] |-> ##1 arr[1]);

endmodule


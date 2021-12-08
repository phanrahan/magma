module Reverse (
    input [3:0] I,
    output [3:0] O
);
assign O = {I[0],I[1],I[2],I[3]};
endmodule

module Foo (
    input [3:0] I,
    output [3:0] O
);
wire [3:0] Reverse_inst0_O;
Reverse Reverse_inst0 (
    .I(I),
    .O(Reverse_inst0_O)
);
assign O = Reverse_inst0_O;
endmodule


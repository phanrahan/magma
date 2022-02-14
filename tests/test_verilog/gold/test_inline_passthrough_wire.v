module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module corebit_term (
    input in
);

endmodule

module Foo (
    input I_x,
    input [3:0] I_y,
    output O_x,
    output [3:0] O_y
);
wire _magma_inline_wire0;
wire _magma_inline_wire1;
wire [1:0] _magma_inline_wire2;
wire [1:0] _magma_inline_wire3;
assign _magma_inline_wire0 = I_y[0];
assign _magma_inline_wire1 = I_y[1];
assign _magma_inline_wire2 = {I_y[2],I_y[1]};
assign _magma_inline_wire3 = {I_y[3],I_y[2]};
assign O_x = I_x;
assign O_y = I_y;

    assert _magma_inline_wire0 == _magma_inline_wire1


    assert _magma_inline_wire2 == _magma_inline_wire3

endmodule


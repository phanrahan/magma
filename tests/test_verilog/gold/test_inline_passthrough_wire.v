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
assign O_x = I_x;
assign O_y = I_y;

    assert I_y[0] == I_y[1]


    assert {I_y[2],I_y[1]} == {I_y[3],I_y[2]}

endmodule


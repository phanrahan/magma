module Foo (
    input [3:0] I_c_0_a [3:0],
    input [3:0] I_c_1_a [3:0],
    output [3:0] O_c_0_a [3:0],
    output [3:0] O_c_1_a [3:0]
);
assign O_c_0_a[3] = I_c_1_a[0];
assign O_c_0_a[2] = I_c_1_a[1];
assign O_c_0_a[1] = I_c_1_a[2];
assign O_c_0_a[0] = I_c_1_a[3];
assign O_c_1_a[3] = I_c_0_a[0];
assign O_c_1_a[2] = I_c_0_a[1];
assign O_c_1_a[1] = I_c_0_a[2];
assign O_c_1_a[0] = I_c_0_a[3];
endmodule


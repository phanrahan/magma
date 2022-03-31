module Foo (
    input I_0_x,
    output I_0_y,
    input I_1_x,
    output I_1_y,
    input I_2_x,
    output I_2_y,
    input I_3_x,
    output I_3_y,
    output O_0_x,
    input O_0_y,
    output O_1_x,
    input O_1_y,
    output O_2_x,
    input O_2_y,
    output O_3_x,
    input O_3_y
);
assign I_0_y = O_2_y;
assign I_1_y = O_3_y;
assign I_2_y = O_0_y;
assign I_3_y = O_1_y;
assign O_0_x = I_2_x;
assign O_1_x = I_3_x;
assign O_2_x = I_0_x;
assign O_3_x = I_1_x;
endmodule


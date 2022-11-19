module main (input  I0_x, input  I0_y, input  I1_x, input  I1_y, output  O_x, output  O_y);
wire  and2_I0_x;
wire  and2_I0_y;
wire  and2_I1_x;
wire  and2_I1_y;
wire  and2_O_x;
wire  and2_O_y;
And2 and2 (.I0_x(I0_x), .I0_y(I0_y), .I1_x(I1_x), .I1_y(I1_y), .O_x(and2_O_x), .O_y(and2_O_y));
assign O_x = and2_O_x;
assign O_y = and2_O_y;
endmodule


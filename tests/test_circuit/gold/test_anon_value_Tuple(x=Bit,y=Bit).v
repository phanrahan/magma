module main (input  I0_x, input  I0_y, input  I1_x, input  I1_y, output  O_x, output  O_y);
wire  And2_inst0_I0_x;
wire  And2_inst0_I0_y;
wire  And2_inst0_I1_x;
wire  And2_inst0_I1_y;
wire  And2_inst0_O_x;
wire  And2_inst0_O_y;
And2 And2_inst0 (.I0_x(I0_x), .I0_y(I0_y), .I1_x(I1_x), .I1_y(I1_y), .O_x(And2_inst0_O_x), .O_y(And2_inst0_O_y));
assign O_x = And2_inst0_O_x;
assign O_y = And2_inst0_O_y;
endmodule


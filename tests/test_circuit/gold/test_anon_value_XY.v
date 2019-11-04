module main (input  I0_x, input  I0_y, input  I1_x, input  I1_y, output  O_x, output  O_y);
wire  And2_inst0_I0_x;
wire  And2_inst0_I0_y;
wire  And2_inst0_I1_x;
wire  And2_inst0_I1_y;
wire  And2_inst0_O_x;
wire  And2_inst0_O_y;
And2 And2_inst0 (.I0(I0), .I1(I1), .O(And2_inst0_O));
assign O = And2_inst0_O;
endmodule


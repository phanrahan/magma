module Not (input  I, output  O);
assign O = 1'b0;
endmodule

module logic (input [3:0] a, output [3:0] O);
wire  Not_inst0_O;
wire  Not_inst1_O;
wire  Not_inst2_O;
wire  Not_inst3_O;
Not Not_inst0 (.I(a[3]), .O(Not_inst0_O));
Not Not_inst1 (.I(a[2]), .O(Not_inst1_O));
Not Not_inst2 (.I(a[1]), .O(Not_inst2_O));
Not Not_inst3 (.I(a[0]), .O(Not_inst3_O));
assign O = {Not_inst3_O,a[1],Not_inst1_O,a[3]};
endmodule


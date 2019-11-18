// Module `add` defined externally
module _Add (input [7:0] I0, input [7:0] I1, output [7:0] O);
wire [7:0] add_inst0_O;
add add_inst0(.I0(I0), .I1(I1), .O(add_inst0_O));
assign O = add_inst0_O;
endmodule

module Top (input [7:0] I0, input [7:0] I1, output [7:0] O);
wire [7:0] _Add_inst0_O;
_Add _Add_inst0(.I0(I0), .I1(I1), .O(_Add_inst0_O));
assign O = _Add_inst0_O;
endmodule


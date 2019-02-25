module Not (input  I, output  O);
assign O = 1'b0;
endmodule

module invert (input  a, output  O);
wire  Not_inst0_O;
Not Not_inst0 (.I(a), .O(Not_inst0_O));
assign O = Not_inst0_O;
endmodule

module Foo (input  I, output  O);
wire  invert_inst0_O;
invert invert_inst0 (.a(I), .O(invert_inst0_O));
assign O = invert_inst0_O;
endmodule


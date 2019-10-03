module logic (input [3:0] a, output [3:0] O);
assign O = {a[0],a[1],a[2],a[3]};
endmodule

module Foo (input [3:0] a, output [3:0] c);
wire [3:0] logic_inst0_O;
logic logic_inst0 (.a(a), .O(logic_inst0_O));
assign c = logic_inst0_O;
endmodule


// Module `AddPrim` defined externally
module _Add (
    input [7:0] I0,
    input [7:0] I1,
    output [7:0] O
);
wire [7:0] AddPrim_inst0_I0;
wire [7:0] AddPrim_inst0_I1;
wire [7:0] AddPrim_inst0_O;
assign AddPrim_inst0_I0 = I0;
assign AddPrim_inst0_I1 = I1;
AddPrim AddPrim_inst0 (
    .I0(AddPrim_inst0_I0),
    .I1(AddPrim_inst0_I1),
    .O(AddPrim_inst0_O)
);
assign O = AddPrim_inst0_O;
endmodule

module Top (
    input [7:0] I0,
    input [7:0] I1,
    output [7:0] O
);
wire [7:0] add8_I0;
wire [7:0] add8_I1;
wire [7:0] add8_O;
assign add8_I0 = I0;
assign add8_I1 = I1;
_Add add8 (
    .I0(add8_I0),
    .I1(add8_I1),
    .O(add8_O)
);
assign O = add8_O;
endmodule


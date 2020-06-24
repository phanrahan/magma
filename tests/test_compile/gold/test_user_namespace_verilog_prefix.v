module my_namespace_Bar (
    input I_x,
    input I_y,
    output O_x,
    output O_y
);
assign O_x = I_x;
assign O_y = I_y;
endmodule

module my_namespace_Foo (
    input I_x,
    input I_y,
    output O_x,
    output O_y
);
wire Bar_inst0_O_x;
wire Bar_inst0_O_y;
Bar Bar_inst0 (
    .I_x(I_x),
    .I_y(I_y),
    .O_x(Bar_inst0_O_x),
    .O_y(Bar_inst0_O_y)
);
assign O_x = Bar_inst0_O_x;
assign O_y = Bar_inst0_O_y;
endmodule


// Module `Foo` defined externally
module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
endmodule

module Main (
    input [4:0] I__0,
    input I__1,
    output [4:0] O__0,
    output O__1
);
wire [4:0] Foo_inst0_O__0;
wire Foo_inst0_O__1;
wire [5:0] x_out;
Foo Foo_inst0 (
    .I__0(I__0),
    .I__1(I__1),
    .O__0(Foo_inst0_O__0),
    .O__1(Foo_inst0_O__1)
);
coreir_wire #(
    .width(6)
) x (
    .in({Foo_inst0_O__1,Foo_inst0_O__0[4],Foo_inst0_O__0[3],Foo_inst0_O__0[2],Foo_inst0_O__0[1],Foo_inst0_O__0[0]}),
    .out(x_out)
);
assign O__0 = {x_out[4],x_out[3],x_out[2],x_out[1],x_out[0]};
assign O__1 = x_out[5];
endmodule


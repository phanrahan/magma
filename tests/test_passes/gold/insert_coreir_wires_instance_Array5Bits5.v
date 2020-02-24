// Module `Foo` defined externally
module Main (
    input [4:0] I_0,
    input [4:0] I_1,
    input [4:0] I_2,
    input [4:0] I_3,
    input [4:0] I_4,
    output [4:0] O_0,
    output [4:0] O_1,
    output [4:0] O_2,
    output [4:0] O_3,
    output [4:0] O_4
);
wire [4:0] Foo_inst0_O_0;
wire [4:0] Foo_inst0_O_1;
wire [4:0] Foo_inst0_O_2;
wire [4:0] Foo_inst0_O_3;
wire [4:0] Foo_inst0_O_4;
wire [24:0] x;
Foo Foo_inst0 (
    .I_0(I_0),
    .I_1(I_1),
    .I_2(I_2),
    .I_3(I_3),
    .I_4(I_4),
    .O_0(Foo_inst0_O_0),
    .O_1(Foo_inst0_O_1),
    .O_2(Foo_inst0_O_2),
    .O_3(Foo_inst0_O_3),
    .O_4(Foo_inst0_O_4)
);
assign x = {Foo_inst0_O_4[4],Foo_inst0_O_4[3],Foo_inst0_O_4[2],Foo_inst0_O_4[1],Foo_inst0_O_4[0],Foo_inst0_O_3[4],Foo_inst0_O_3[3],Foo_inst0_O_3[2],Foo_inst0_O_3[1],Foo_inst0_O_3[0],Foo_inst0_O_2[4],Foo_inst0_O_2[3],Foo_inst0_O_2[2],Foo_inst0_O_2[1],Foo_inst0_O_2[0],Foo_inst0_O_1[4],Foo_inst0_O_1[3],Foo_inst0_O_1[2],Foo_inst0_O_1[1],Foo_inst0_O_1[0],Foo_inst0_O_0[4],Foo_inst0_O_0[3],Foo_inst0_O_0[2],Foo_inst0_O_0[1],Foo_inst0_O_0[0]};
assign O_0 = {x[4],x[3],x[2],x[1],x[0]};
assign O_1 = {x[9],x[8],x[7],x[6],x[5]};
assign O_2 = {x[14],x[13],x[12],x[11],x[10]};
assign O_3 = {x[19],x[18],x[17],x[16],x[15]};
assign O_4 = {x[24],x[23],x[22],x[21],x[20]};
endmodule


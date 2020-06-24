// Module `Foo` defined externally
module mantle_wire__typeBitIn5 (
    output [4:0] in,
    input [4:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit5 (
    input [4:0] in,
    output [4:0] out
);
assign out = in;
endmodule

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
wire [4:0] _$0_out;
wire [4:0] _$1_out;
wire [4:0] _$2_out;
wire [4:0] _$3_out;
wire [4:0] _$4_out;
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
mantle_wire__typeBit5 _$0 (
    .in(Foo_inst0_O_0),
    .out(_$0_out)
);
mantle_wire__typeBit5 _$1 (
    .in(Foo_inst0_O_1),
    .out(_$1_out)
);
mantle_wire__typeBit5 _$2 (
    .in(Foo_inst0_O_2),
    .out(_$2_out)
);
mantle_wire__typeBit5 _$3 (
    .in(Foo_inst0_O_3),
    .out(_$3_out)
);
mantle_wire__typeBit5 _$4 (
    .in(Foo_inst0_O_4),
    .out(_$4_out)
);
mantle_wire__typeBitIn5 _$5 (
    .in(O_0),
    .out(x[4:0])
);
mantle_wire__typeBitIn5 _$6 (
    .in(O_1),
    .out(x[9:5])
);
mantle_wire__typeBitIn5 _$7 (
    .in(O_2),
    .out(x[14:10])
);
mantle_wire__typeBitIn5 _$8 (
    .in(O_3),
    .out(x[19:15])
);
mantle_wire__typeBitIn5 _$9 (
    .in(O_4),
    .out(x[24:20])
);
assign x = {_$4_out[4:0],_$3_out[4:0],_$2_out[4:0],_$1_out[4:0],_$0_out[4:0]};
endmodule


module mantle_wire__typeBitIn3 (
    output [2:0] in,
    input [2:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn2 (
    output [1:0] in,
    input [1:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit3 (
    input [2:0] in,
    output [2:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit2 (
    input [1:0] in,
    output [1:0] out
);
assign out = in;
endmodule

module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module commonlib_muxn__N2__width3 (
    input [2:0] in_data [1:0],
    input [0:0] in_sel,
    output [2:0] out
);
wire [2:0] _join_out;
coreir_mux #(
    .width(3)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTupleBit_Bits2 (
    input I0__0,
    input [1:0] I0__1,
    input I1__0,
    input [1:0] I1__1,
    output O__0,
    output [1:0] O__1,
    input S
);
wire [2:0] coreir_commonlib_mux2x3_inst0_out;
wire [2:0] coreir_commonlib_mux2x3_inst0_in_data_0_in;
wire [2:0] coreir_commonlib_mux2x3_inst0_in_data_1_in;
wire [2:0] coreir_commonlib_mux2x3_inst0_out_wire_out;
wire [1:0] self_I0__1_wire_out;
wire [1:0] self_I1__1_wire_out;
wire [1:0] self_O__1_wire_in;
wire [2:0] coreir_commonlib_mux2x3_inst0_in_data [1:0];
assign coreir_commonlib_mux2x3_inst0_in_data[1] = coreir_commonlib_mux2x3_inst0_in_data_1_in;
assign coreir_commonlib_mux2x3_inst0_in_data[0] = coreir_commonlib_mux2x3_inst0_in_data_0_in;
commonlib_muxn__N2__width3 coreir_commonlib_mux2x3_inst0 (
    .in_data(coreir_commonlib_mux2x3_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x3_inst0_out)
);
wire [2:0] coreir_commonlib_mux2x3_inst0_in_data_0_out;
assign coreir_commonlib_mux2x3_inst0_in_data_0_out = {self_I0__1_wire_out[1:0],I0__0};
mantle_wire__typeBitIn3 coreir_commonlib_mux2x3_inst0_in_data_0 (
    .in(coreir_commonlib_mux2x3_inst0_in_data_0_in),
    .out(coreir_commonlib_mux2x3_inst0_in_data_0_out)
);
wire [2:0] coreir_commonlib_mux2x3_inst0_in_data_1_out;
assign coreir_commonlib_mux2x3_inst0_in_data_1_out = {self_I1__1_wire_out[1:0],I1__0};
mantle_wire__typeBitIn3 coreir_commonlib_mux2x3_inst0_in_data_1 (
    .in(coreir_commonlib_mux2x3_inst0_in_data_1_in),
    .out(coreir_commonlib_mux2x3_inst0_in_data_1_out)
);
mantle_wire__typeBit3 coreir_commonlib_mux2x3_inst0_out_wire (
    .in(coreir_commonlib_mux2x3_inst0_out),
    .out(coreir_commonlib_mux2x3_inst0_out_wire_out)
);
mantle_wire__typeBit2 self_I0__1_wire (
    .in(I0__1),
    .out(self_I0__1_wire_out)
);
mantle_wire__typeBit2 self_I1__1_wire (
    .in(I1__1),
    .out(self_I1__1_wire_out)
);
mantle_wire__typeBitIn2 self_O__1_wire (
    .in(self_O__1_wire_in),
    .out(coreir_commonlib_mux2x3_inst0_out_wire_out[2:1])
);
assign O__0 = coreir_commonlib_mux2x3_inst0_out_wire_out[0];
assign O__1 = self_O__1_wire_in;
endmodule

module test_basic_mux_tuple (
    input I_0__0,
    input [1:0] I_0__1,
    input I_1__0,
    input [1:0] I_1__1,
    output O__0,
    output [1:0] O__1,
    input S
);
wire Mux2xTupleBit_Bits2_inst0_O__0;
wire [1:0] Mux2xTupleBit_Bits2_inst0_O__1;
Mux2xTupleBit_Bits2 Mux2xTupleBit_Bits2_inst0 (
    .I0__0(I_0__0),
    .I0__1(I_0__1),
    .I1__0(I_1__0),
    .I1__1(I_1__1),
    .O__0(Mux2xTupleBit_Bits2_inst0_O__0),
    .O__1(Mux2xTupleBit_Bits2_inst0_O__1),
    .S(S)
);
assign O__0 = Mux2xTupleBit_Bits2_inst0_O__0;
assign O__1 = Mux2xTupleBit_Bits2_inst0_O__1;
endmodule


module slice_2_4_Array_4_Array_4_OutBit (
    input [3:0] I [3:0],
    output [3:0] O [1:0]
);
assign O[1] = I[3];
assign O[0] = I[2];
endmodule

module slice_0_2_Array_4_Array_4_OutBit (
    input [3:0] I [3:0],
    output [3:0] O [1:0]
);
assign O[1] = I[1];
assign O[0] = I[0];
endmodule

module coreir_concat #(
    parameter width0 = 1,
    parameter width1 = 1
) (
    input [width0-1:0] in0,
    input [width1-1:0] in1,
    output [width0+width1-1:0] out
);
  assign out = {in1,in0};
endmodule

module Concat (
    input [3:0] I0 [1:0],
    input [3:0] I1 [1:0],
    output [3:0] O [3:0]
);
wire [15:0] Concat_inst0_out;
wire [7:0] Concat_inst0_in0;
assign Concat_inst0_in0 = {I0[1][3:0],I0[0][3:0]};
wire [7:0] Concat_inst0_in1;
assign Concat_inst0_in1 = {I1[1][3:0],I1[0][3:0]};
coreir_concat #(
    .width0(8),
    .width1(8)
) Concat_inst0 (
    .in0(Concat_inst0_in0),
    .in1(Concat_inst0_in1),
    .out(Concat_inst0_out)
);
assign O[3] = {Concat_inst0_out[15],Concat_inst0_out[14],Concat_inst0_out[13],Concat_inst0_out[12]};
assign O[2] = {Concat_inst0_out[11],Concat_inst0_out[10],Concat_inst0_out[9],Concat_inst0_out[8]};
assign O[1] = {Concat_inst0_out[7],Concat_inst0_out[6],Concat_inst0_out[5],Concat_inst0_out[4]};
assign O[0] = {Concat_inst0_out[3],Concat_inst0_out[2],Concat_inst0_out[1],Concat_inst0_out[0]};
endmodule

module Foo (
    input [3:0] I [3:0],
    output [3:0] O [3:0]
);
wire [3:0] Concat_inst0_O [3:0];
wire [3:0] slice_0_2_Array_4_Array_4_OutBit_inst0_O [1:0];
wire [3:0] slice_2_4_Array_4_Array_4_OutBit_inst0_O [1:0];
wire [3:0] Concat_inst0_I0 [1:0];
assign Concat_inst0_I0[1] = slice_2_4_Array_4_Array_4_OutBit_inst0_O[1];
assign Concat_inst0_I0[0] = slice_2_4_Array_4_Array_4_OutBit_inst0_O[0];
wire [3:0] Concat_inst0_I1 [1:0];
assign Concat_inst0_I1[1] = slice_0_2_Array_4_Array_4_OutBit_inst0_O[1];
assign Concat_inst0_I1[0] = slice_0_2_Array_4_Array_4_OutBit_inst0_O[0];
Concat Concat_inst0 (
    .I0(Concat_inst0_I0),
    .I1(Concat_inst0_I1),
    .O(Concat_inst0_O)
);
wire [3:0] slice_0_2_Array_4_Array_4_OutBit_inst0_I [3:0];
assign slice_0_2_Array_4_Array_4_OutBit_inst0_I[3] = I[3];
assign slice_0_2_Array_4_Array_4_OutBit_inst0_I[2] = I[2];
assign slice_0_2_Array_4_Array_4_OutBit_inst0_I[1] = I[1];
assign slice_0_2_Array_4_Array_4_OutBit_inst0_I[0] = I[0];
slice_0_2_Array_4_Array_4_OutBit slice_0_2_Array_4_Array_4_OutBit_inst0 (
    .I(slice_0_2_Array_4_Array_4_OutBit_inst0_I),
    .O(slice_0_2_Array_4_Array_4_OutBit_inst0_O)
);
wire [3:0] slice_2_4_Array_4_Array_4_OutBit_inst0_I [3:0];
assign slice_2_4_Array_4_Array_4_OutBit_inst0_I[3] = I[3];
assign slice_2_4_Array_4_Array_4_OutBit_inst0_I[2] = I[2];
assign slice_2_4_Array_4_Array_4_OutBit_inst0_I[1] = I[1];
assign slice_2_4_Array_4_Array_4_OutBit_inst0_I[0] = I[0];
slice_2_4_Array_4_Array_4_OutBit slice_2_4_Array_4_Array_4_OutBit_inst0 (
    .I(slice_2_4_Array_4_Array_4_OutBit_inst0_I),
    .O(slice_2_4_Array_4_Array_4_OutBit_inst0_O)
);
assign O[3] = Concat_inst0_O[3];
assign O[2] = Concat_inst0_O[2];
assign O[1] = Concat_inst0_O[1];
assign O[0] = Concat_inst0_O[0];
endmodule


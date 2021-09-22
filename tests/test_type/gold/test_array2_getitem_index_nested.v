module slice_1_2_Array_2_Array_2_OutBit (
    input [1:0] I [1:0],
    output [1:0] O [0:0]
);
assign O[0] = I[1];
endmodule

module slice_0_1_Array_2_Array_2_OutBit (
    input [1:0] I [1:0],
    output [1:0] O [0:0]
);
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
    input [1:0] I0 [0:0],
    input [1:0] I1 [0:0],
    output [1:0] O [1:0]
);
wire [3:0] Concat_inst0_out;
coreir_concat #(
    .width0(2),
    .width1(2)
) Concat_inst0 (
    .in0(I0[0]),
    .in1(I1[0]),
    .out(Concat_inst0_out)
);
assign O[1] = {Concat_inst0_out[3],Concat_inst0_out[2]};
assign O[0] = {Concat_inst0_out[1],Concat_inst0_out[0]};
endmodule

module Foo (
    input [1:0] I [1:0],
    output [1:0] O [1:0]
);
wire [1:0] Concat_inst0_O [1:0];
wire [1:0] slice_0_1_Array_2_Array_2_OutBit_inst0_O [0:0];
wire [1:0] slice_1_2_Array_2_Array_2_OutBit_inst0_O [0:0];
wire [1:0] Concat_inst0_I0 [0:0];
assign Concat_inst0_I0[0] = slice_1_2_Array_2_Array_2_OutBit_inst0_O[0];
wire [1:0] Concat_inst0_I1 [0:0];
assign Concat_inst0_I1[0] = slice_0_1_Array_2_Array_2_OutBit_inst0_O[0];
Concat Concat_inst0 (
    .I0(Concat_inst0_I0),
    .I1(Concat_inst0_I1),
    .O(Concat_inst0_O)
);
wire [1:0] slice_0_1_Array_2_Array_2_OutBit_inst0_I [1:0];
assign slice_0_1_Array_2_Array_2_OutBit_inst0_I[1] = I[1];
assign slice_0_1_Array_2_Array_2_OutBit_inst0_I[0] = I[0];
slice_0_1_Array_2_Array_2_OutBit slice_0_1_Array_2_Array_2_OutBit_inst0 (
    .I(slice_0_1_Array_2_Array_2_OutBit_inst0_I),
    .O(slice_0_1_Array_2_Array_2_OutBit_inst0_O)
);
wire [1:0] slice_1_2_Array_2_Array_2_OutBit_inst0_I [1:0];
assign slice_1_2_Array_2_Array_2_OutBit_inst0_I[1] = I[1];
assign slice_1_2_Array_2_Array_2_OutBit_inst0_I[0] = I[0];
slice_1_2_Array_2_Array_2_OutBit slice_1_2_Array_2_Array_2_OutBit_inst0 (
    .I(slice_1_2_Array_2_Array_2_OutBit_inst0_I),
    .O(slice_1_2_Array_2_Array_2_OutBit_inst0_O)
);
assign O[1] = Concat_inst0_O[1];
assign O[0] = Concat_inst0_O[0];
endmodule


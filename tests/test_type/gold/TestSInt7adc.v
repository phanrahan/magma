module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module TestBinary (
    input [6:0] I0,
    input [6:0] I1,
    input CIN,
    output [6:0] O,
    output COUT
);
wire bit_const_0_None_out;
wire [7:0] magma_SInt_8_add_inst0_out;
wire [7:0] magma_SInt_8_add_inst1_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
wire [7:0] magma_SInt_8_add_inst0_in0;
assign magma_SInt_8_add_inst0_in0 = {I0[6],I0};
wire [7:0] magma_SInt_8_add_inst0_in1;
assign magma_SInt_8_add_inst0_in1 = {I1[6],I1};
coreir_add #(
    .width(8)
) magma_SInt_8_add_inst0 (
    .in0(magma_SInt_8_add_inst0_in0),
    .in1(magma_SInt_8_add_inst0_in1),
    .out(magma_SInt_8_add_inst0_out)
);
wire [7:0] magma_SInt_8_add_inst1_in1;
assign magma_SInt_8_add_inst1_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,CIN};
coreir_add #(
    .width(8)
) magma_SInt_8_add_inst1 (
    .in0(magma_SInt_8_add_inst0_out),
    .in1(magma_SInt_8_add_inst1_in1),
    .out(magma_SInt_8_add_inst1_out)
);
assign O = magma_SInt_8_add_inst1_out[6:0];
assign COUT = magma_SInt_8_add_inst1_out[7];
endmodule


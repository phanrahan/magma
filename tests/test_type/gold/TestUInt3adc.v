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
    input [2:0] I0,
    input [2:0] I1,
    input CIN,
    output [2:0] O,
    output COUT
);
wire bit_const_0_None_out;
wire [3:0] magma_UInt_4_add_inst0_out;
wire [3:0] magma_UInt_4_add_inst1_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
wire [3:0] magma_UInt_4_add_inst0_in0;
assign magma_UInt_4_add_inst0_in0 = {bit_const_0_None_out,I0};
wire [3:0] magma_UInt_4_add_inst0_in1;
assign magma_UInt_4_add_inst0_in1 = {bit_const_0_None_out,I1};
coreir_add #(
    .width(4)
) magma_UInt_4_add_inst0 (
    .in0(magma_UInt_4_add_inst0_in0),
    .in1(magma_UInt_4_add_inst0_in1),
    .out(magma_UInt_4_add_inst0_out)
);
wire [3:0] magma_UInt_4_add_inst1_in1;
assign magma_UInt_4_add_inst1_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,CIN};
coreir_add #(
    .width(4)
) magma_UInt_4_add_inst1 (
    .in0(magma_UInt_4_add_inst0_out),
    .in1(magma_UInt_4_add_inst1_in1),
    .out(magma_UInt_4_add_inst1_out)
);
assign O = magma_UInt_4_add_inst1_out[2:0];
assign COUT = magma_UInt_4_add_inst1_out[3];
endmodule


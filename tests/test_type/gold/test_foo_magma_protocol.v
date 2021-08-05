module coreir_shl #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 << in1;
endmodule

module coreir_reg #(
    parameter width = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module coreir_or #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 | in1;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module Register (
    input [0:0] I,
    output [0:0] O,
    input CLK
);
wire [0:0] reg_P1_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P1_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P1_inst0_out)
);
assign O = reg_P1_inst0_out;
endmodule

module Bar (
    input [7:0] foo,
    output [7:0] O,
    input CLK
);
wire [0:0] Register_inst0_O;
wire bit_const_0_None_out;
wire [7:0] const_1_8_out;
wire [7:0] const_2_8_out;
wire [7:0] magma_Bits_8_or_inst0_out;
wire [7:0] magma_Bits_8_or_inst1_out;
wire [7:0] magma_Bits_8_shl_inst0_out;
wire [7:0] magma_Bits_8_shl_inst1_out;
Register Register_inst0 (
    .I(Register_inst0_O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
coreir_const #(
    .value(8'h02),
    .width(8)
) const_2_8 (
    .out(const_2_8_out)
);
coreir_or #(
    .width(8)
) magma_Bits_8_or_inst0 (
    .in0(magma_Bits_8_shl_inst0_out),
    .in1(magma_Bits_8_shl_inst1_out),
    .out(magma_Bits_8_or_inst0_out)
);
wire [7:0] magma_Bits_8_or_inst1_in1;
assign magma_Bits_8_or_inst1_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,foo[0]};
coreir_or #(
    .width(8)
) magma_Bits_8_or_inst1 (
    .in0(magma_Bits_8_or_inst0_out),
    .in1(magma_Bits_8_or_inst1_in1),
    .out(magma_Bits_8_or_inst1_out)
);
coreir_shl #(
    .width(8)
) magma_Bits_8_shl_inst0 (
    .in0(foo),
    .in1(const_2_8_out),
    .out(magma_Bits_8_shl_inst0_out)
);
wire [7:0] magma_Bits_8_shl_inst1_in0;
assign magma_Bits_8_shl_inst1_in0 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,foo[0]};
coreir_shl #(
    .width(8)
) magma_Bits_8_shl_inst1 (
    .in0(magma_Bits_8_shl_inst1_in0),
    .in1(const_1_8_out),
    .out(magma_Bits_8_shl_inst1_out)
);
assign O = magma_Bits_8_or_inst1_out;
endmodule


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

module Register (
    input [7:0] I,
    output [7:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P8_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Foo (
    input [7:0] write_pointer,
    output [7:0] O [3:0],
    input CLK
);
wire [7:0] Register_inst0_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire [7:0] magma_UInt_8_add_inst0_out;
wire [7:0] magma_UInt_8_add_inst1_out;
wire [7:0] magma_UInt_8_add_inst2_out;
wire [7:0] magma_UInt_8_add_inst3_out;
wire [31:0] pointer;
wire [7:0] pointer_0;
wire [7:0] pointer_1;
wire [7:0] pointer_2;
wire [7:0] pointer_3;
Register Register_inst0 (
    .I(write_pointer),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign magma_Bit_and_inst0_out = pointer_0[7] & 1'b1;
assign magma_Bit_and_inst1_out = pointer_1[7] & 1'b1;
assign magma_Bit_and_inst2_out = pointer_2[7] & 1'b1;
assign magma_Bit_and_inst3_out = pointer_3[7] & 1'b1;
assign magma_UInt_8_add_inst0_out = 8'(Register_inst0_O + 8'h00);
assign magma_UInt_8_add_inst1_out = 8'(Register_inst0_O + 8'h01);
assign magma_UInt_8_add_inst2_out = 8'(Register_inst0_O + 8'h02);
assign magma_UInt_8_add_inst3_out = 8'(Register_inst0_O + 8'h03);
assign pointer = {magma_UInt_8_add_inst3_out,magma_UInt_8_add_inst2_out,magma_UInt_8_add_inst1_out,magma_UInt_8_add_inst0_out};
assign pointer_0 = magma_UInt_8_add_inst0_out;
assign pointer_1 = magma_UInt_8_add_inst1_out;
assign pointer_2 = magma_UInt_8_add_inst2_out;
assign pointer_3 = magma_UInt_8_add_inst3_out;
assign O[3] = {pointer[31],pointer[30],pointer[29],pointer[28],pointer[27],pointer[26],pointer[25],pointer[24]};
assign O[2] = {pointer[23],pointer[22],pointer[21],pointer[20],pointer[19],pointer[18],pointer[17],pointer[16]};
assign O[1] = {pointer[15],pointer[14],pointer[13],pointer[12],pointer[11],pointer[10],pointer[9],pointer[8]};
assign O[0] = {pointer[7],pointer[6],pointer[5],pointer[4],pointer[3],pointer[2],pointer[1],pointer[0]};
endmodule


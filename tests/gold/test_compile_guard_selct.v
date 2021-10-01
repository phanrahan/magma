// Module `_CompileGuardSelect` defined externally
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

module corebit_xor (
    input in0,
    input in1,
    output out
);
  assign out = in0 ^ in1;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module Register (
    input I,
    output O,
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
assign O = reg_P1_inst0_out[0];
endmodule

module _Top (
    input I,
    output O,
    input CLK
);
wire Register_inst0_O;
wire Register_inst1_O;
wire _CompileGuardSelect_inst0_O;
wire bit_const_1_None_out;
wire magma_Bit_xor_inst0_out;
Register Register_inst0 (
    .I(magma_Bit_xor_inst0_out),
    .O(Register_inst0_O),
    .CLK(CLK)
);
Register Register_inst1 (
    .I(I),
    .O(Register_inst1_O),
    .CLK(CLK)
);
_CompileGuardSelect _CompileGuardSelect_inst0 (
    .I0(Register_inst0_O),
    .I1(Register_inst1_O),
    .I2(I),
    .O(_CompileGuardSelect_inst0_O)
);
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
corebit_xor magma_Bit_xor_inst0 (
    .in0(I),
    .in1(bit_const_1_None_out),
    .out(magma_Bit_xor_inst0_out)
);
assign O = _CompileGuardSelect_inst0_O;
endmodule


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

module CompileGuardSelect_Bit_COND1_COND2_default (
    input I0,
    input I1,
    input I2,
    output O
);
`ifdef COND1
    assign O = I0;
`elsif COND2
    assign O = I1;
`else
    assign O = I2;
`endif
endmodule

module _Top (
    input I,
    output O,
    input CLK
);
wire Register_inst0_O;
wire Register_inst1_O;
wire magma_Bit_xor_inst0_out;
CompileGuardSelect_Bit_COND1_COND2_default CompileGuardSelect_Bit_COND1_COND2_default_inst0 (
    .I0(Register_inst0_O),
    .I1(Register_inst1_O),
    .I2(I),
    .O(O)
);
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
assign magma_Bit_xor_inst0_out = I ^ 1'b1;
endmodule


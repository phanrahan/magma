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
    input [15:0] I,
    output [15:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(16'h0000),
    .width(16)
) reg_P_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Test2 (
    input sel,
    output [15:0] O,
    input CLK
);
wire [15:0] Register_inst0_O;
wire [15:0] magma_Bit_ite_Out_SInt_16_inst0_out;
Register Register_inst0 (
    .I(magma_Bit_ite_Out_SInt_16_inst0_out),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign magma_Bit_ite_Out_SInt_16_inst0_out = sel ? 16'(Register_inst0_O + 16'h0001) : Register_inst0_O;
assign O = magma_Bit_ite_Out_SInt_16_inst0_out;
endmodule


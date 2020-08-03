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
wire reg_P_inst0_clk;
wire [15:0] reg_P_inst0_in;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(16'h0000),
    .width(16)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(O)
);
endmodule

module Test2 (
    output [15:0] O,
    input CLK
);
wire [15:0] Register_inst0_I;
wire [15:0] Register_inst0_O;
wire Register_inst0_CLK;
wire [15:0] magma_Bits_16_add_inst0_out;
assign Register_inst0_I = magma_Bits_16_add_inst0_out;
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK)
);
assign magma_Bits_16_add_inst0_out = 16'(Register_inst0_O + 16'h0001);
assign O = magma_Bits_16_add_inst0_out;
endmodule


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
) reg_P16_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Mux2x_SequentialRegisterWrapperSInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input S,
    output [15:0] O
);
reg [15:0] coreir_commonlib_mux2x16_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x16_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x16_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x16_inst0_out;
endmodule

module Test2 (
    input sel,
    output [15:0] O,
    input CLK
);
wire [15:0] Register_inst0_O;
wire [15:0] magma_SInt_16_add_inst0_out;
Mux2x_SequentialRegisterWrapperSInt16 Mux2x_SequentialRegisterWrapperSInt16_inst0 (
    .I0(Register_inst0_O),
    .I1(magma_SInt_16_add_inst0_out),
    .S(sel),
    .O(O)
);
Register Register_inst0 (
    .I(O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign magma_SInt_16_add_inst0_out = 16'(Register_inst0_O + 16'h0001);
endmodule


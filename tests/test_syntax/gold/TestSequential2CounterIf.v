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

module Mux2xOutSInt16 (
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
wire [15:0] Mux2xOutSInt16_inst0_I0;
wire [15:0] Mux2xOutSInt16_inst0_I1;
wire Mux2xOutSInt16_inst0_S;
wire [15:0] Register_inst0_I;
wire [15:0] Register_inst0_O;
wire Register_inst0_CLK;
assign Mux2xOutSInt16_inst0_I0 = Register_inst0_O;
assign Mux2xOutSInt16_inst0_I1 = 16'(Register_inst0_O + 16'h0001);
assign Mux2xOutSInt16_inst0_S = sel;
Mux2xOutSInt16 Mux2xOutSInt16_inst0 (
    .I0(Mux2xOutSInt16_inst0_I0),
    .I1(Mux2xOutSInt16_inst0_I1),
    .S(Mux2xOutSInt16_inst0_S),
    .O(O)
);
assign Register_inst0_I = O;
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK)
);
endmodule


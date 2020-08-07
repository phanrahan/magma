module coreir_reg_arst #(
    parameter width = 1,
    parameter arst_posedge = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input arst,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg;
  wire real_rst;
  assign real_rst = arst_posedge ? arst : ~arst;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk, posedge real_rst) begin
    if (real_rst) outReg <= init;
    else outReg <= in;
  end
  assign out = outReg;
endmodule

module Mux2xUInt3 (
    input [2:0] I0,
    input [2:0] I1,
    input S,
    output [2:0] O
);
reg [2:0] coreir_commonlib_mux2x3_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x3_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x3_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x3_inst0_out;
endmodule

module Register (
    input [2:0] I,
    output [2:0] O,
    input CLK,
    input CE,
    input ASYNCRESET
);
wire [2:0] enable_mux_I0;
wire [2:0] enable_mux_I1;
wire enable_mux_S;
wire [2:0] enable_mux_O;
wire reg_PR_inst0_clk;
wire reg_PR_inst0_arst;
wire [2:0] reg_PR_inst0_in;
assign enable_mux_I0 = O;
assign enable_mux_I1 = I;
assign enable_mux_S = CE;
Mux2xUInt3 enable_mux (
    .I0(enable_mux_I0),
    .I1(enable_mux_I1),
    .S(enable_mux_S),
    .O(enable_mux_O)
);
assign reg_PR_inst0_clk = CLK;
assign reg_PR_inst0_arst = ASYNCRESET;
assign reg_PR_inst0_in = enable_mux_O;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
    .out(O)
);
endmodule

module Test2 (
    output [2:0] O,
    input CLK,
    input CE,
    input ASYNCRESET
);
wire [2:0] Register_inst0_I;
wire [2:0] Register_inst0_O;
wire Register_inst0_CLK;
wire Register_inst0_CE;
wire Register_inst0_ASYNCRESET;
wire [2:0] magma_Bits_3_add_inst0_out;
assign Register_inst0_I = magma_Bits_3_add_inst0_out;
assign Register_inst0_CLK = CLK;
assign Register_inst0_CE = CE;
assign Register_inst0_ASYNCRESET = ASYNCRESET;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK),
    .CE(Register_inst0_CE),
    .ASYNCRESET(Register_inst0_ASYNCRESET)
);
assign magma_Bits_3_add_inst0_out = 3'(Register_inst0_O + 3'h1);
assign O = magma_Bits_3_add_inst0_out;
endmodule


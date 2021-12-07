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
    input CE,
    input CLK,
    input ASYNCRESET
);
wire [2:0] enable_mux_O;
Mux2xUInt3 enable_mux (
    .I0(O),
    .I1(I),
    .S(CE),
    .O(enable_mux_O)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_PR3_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(enable_mux_O),
    .out(O)
);
endmodule

module Test2 (
    output [2:0] O,
    input CLK,
    input CE,
    input ASYNCRESET
);
wire [2:0] Register_inst0_O;
wire [2:0] magma_UInt_3_add_inst0_out;
Register Register_inst0 (
    .I(magma_UInt_3_add_inst0_out),
    .O(Register_inst0_O),
    .CE(CE),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET)
);
assign magma_UInt_3_add_inst0_out = 3'(Register_inst0_O + 3'h1);
assign O = magma_UInt_3_add_inst0_out;
endmodule


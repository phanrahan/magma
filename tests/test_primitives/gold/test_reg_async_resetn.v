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

module Register (
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input ASYNCRESETN
);
wire reg_PR_inst0_clk;
wire reg_PR_inst0_arst;
wire [7:0] reg_PR_inst0_in;
wire [7:0] reg_PR_inst0_out;
assign reg_PR_inst0_clk = CLK;
assign reg_PR_inst0_arst = ASYNCRESETN;
assign reg_PR_inst0_in = I;
coreir_reg_arst #(
    .arst_posedge(1'b0),
    .clk_posedge(1'b1),
    .init(8'hde),
    .width(8)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
    .out(reg_PR_inst0_out)
);
assign O = reg_PR_inst0_out;
endmodule

module test_reg_async_resetn (
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input ASYNCRESETN
);
wire [7:0] Register_inst0_I;
wire [7:0] Register_inst0_O;
wire Register_inst0_CLK;
wire Register_inst0_ASYNCRESETN;
assign Register_inst0_I = I;
assign Register_inst0_CLK = CLK;
assign Register_inst0_ASYNCRESETN = ASYNCRESETN;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK),
    .ASYNCRESETN(Register_inst0_ASYNCRESETN)
);
assign O = Register_inst0_O;
endmodule


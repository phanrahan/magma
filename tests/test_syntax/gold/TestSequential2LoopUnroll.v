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

module LoopUnroll (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] reg_P_inst0_out;
wire [3:0] reg_P_inst1_out;
wire [3:0] reg_P_inst2_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst1 (
    .clk(CLK),
    .in(reg_P_inst0_out),
    .out(reg_P_inst1_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst2 (
    .clk(CLK),
    .in(reg_P_inst1_out),
    .out(reg_P_inst2_out)
);
assign O = reg_P_inst2_out;
endmodule


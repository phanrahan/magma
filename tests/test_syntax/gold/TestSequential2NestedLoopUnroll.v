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
wire reg_P_inst0_clk;
wire [3:0] reg_P_inst0_in;
wire [3:0] reg_P_inst0_out;
wire reg_P_inst1_clk;
wire [3:0] reg_P_inst1_in;
wire [3:0] reg_P_inst1_out;
wire reg_P_inst2_clk;
wire [3:0] reg_P_inst2_in;
wire [3:0] reg_P_inst2_out;
wire reg_P_inst3_clk;
wire [3:0] reg_P_inst3_in;
wire [3:0] reg_P_inst3_out;
wire reg_P_inst4_clk;
wire [3:0] reg_P_inst4_in;
wire [3:0] reg_P_inst4_out;
wire reg_P_inst5_clk;
wire [3:0] reg_P_inst5_in;
wire [3:0] reg_P_inst5_out;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign reg_P_inst1_clk = CLK;
assign reg_P_inst1_in = reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst1 (
    .clk(reg_P_inst1_clk),
    .in(reg_P_inst1_in),
    .out(reg_P_inst1_out)
);
assign reg_P_inst2_clk = CLK;
assign reg_P_inst2_in = reg_P_inst1_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst2 (
    .clk(reg_P_inst2_clk),
    .in(reg_P_inst2_in),
    .out(reg_P_inst2_out)
);
assign reg_P_inst3_clk = CLK;
assign reg_P_inst3_in = reg_P_inst2_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst3 (
    .clk(reg_P_inst3_clk),
    .in(reg_P_inst3_in),
    .out(reg_P_inst3_out)
);
assign reg_P_inst4_clk = CLK;
assign reg_P_inst4_in = reg_P_inst3_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst4 (
    .clk(reg_P_inst4_clk),
    .in(reg_P_inst4_in),
    .out(reg_P_inst4_out)
);
assign reg_P_inst5_clk = CLK;
assign reg_P_inst5_in = reg_P_inst4_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst5 (
    .clk(reg_P_inst5_clk),
    .in(reg_P_inst5_in),
    .out(reg_P_inst5_out)
);
assign O = reg_P_inst5_out;
endmodule


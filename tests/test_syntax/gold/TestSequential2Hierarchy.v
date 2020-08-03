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

module Foo (
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
assign O = reg_P_inst1_out;
endmodule

module Bar (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] Foo_inst0_I;
wire [3:0] Foo_inst0_O;
wire Foo_inst0_CLK;
wire [3:0] Foo_inst1_I;
wire [3:0] Foo_inst1_O;
wire Foo_inst1_CLK;
assign Foo_inst0_I = I;
assign Foo_inst0_CLK = CLK;
Foo Foo_inst0 (
    .I(Foo_inst0_I),
    .O(Foo_inst0_O),
    .CLK(Foo_inst0_CLK)
);
assign Foo_inst1_I = Foo_inst0_O;
assign Foo_inst1_CLK = CLK;
Foo Foo_inst1 (
    .I(Foo_inst1_I),
    .O(Foo_inst1_O),
    .CLK(Foo_inst1_CLK)
);
assign O = Foo_inst1_O;
endmodule


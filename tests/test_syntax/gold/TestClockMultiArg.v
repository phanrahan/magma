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

module TestClockMultiArg_comb (
    input CLK,
    input CLK2,
    input [0:0] self_x_O,
    output [0:0] O0,
    output O1
);
assign O0 = self_x_O;
assign O1 = self_x_O[0];
endmodule

module TestClockMultiArg (
    input CLK,
    input CLK2,
    output O
);
wire [0:0] TestClockMultiArg_comb_inst0_O0;
wire TestClockMultiArg_comb_inst0_O1;
wire [0:0] reg_P_inst0_out;
TestClockMultiArg_comb TestClockMultiArg_comb_inst0 (
    .CLK(CLK),
    .CLK2(CLK2),
    .self_x_O(reg_P_inst0_out),
    .O0(TestClockMultiArg_comb_inst0_O0),
    .O1(TestClockMultiArg_comb_inst0_O1)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P_inst0 (
    .clk(CLK),
    .in(TestClockMultiArg_comb_inst0_O0),
    .out(reg_P_inst0_out)
);
assign O = TestClockMultiArg_comb_inst0_O1;
endmodule


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

module TestClockArg_comb (
    input CLK,
    input [0:0] self_x_O,
    output [0:0] O0,
    output O1
);
assign O0 = self_x_O;
assign O1 = self_x_O[0];
endmodule

module TestClockArg (
    input CLK,
    output O
);
wire [0:0] TestClockArg_comb_inst0_O0;
wire TestClockArg_comb_inst0_O1;
wire [0:0] reg_P_inst0_out;
TestClockArg_comb TestClockArg_comb_inst0 (
    .CLK(CLK),
    .self_x_O(reg_P_inst0_out),
    .O0(TestClockArg_comb_inst0_O0),
    .O1(TestClockArg_comb_inst0_O1)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P_inst0 (
    .clk(CLK),
    .in(TestClockArg_comb_inst0_O0),
    .out(reg_P_inst0_out)
);
assign O = TestClockArg_comb_inst0_O1;
endmodule


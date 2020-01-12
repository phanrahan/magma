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

module TestInitClockArg_comb (
    input CLK,
    input [0:0] self_x_O,
    output [0:0] O0,
    output O1
);
assign O0 = self_x_O;
assign O1 = self_x_O[0];
endmodule

module TestInitClockArg (
    input CLK2,
    input CLK,
    output O
);
wire [0:0] TestInitClockArg_comb_inst0_O0;
wire TestInitClockArg_comb_inst0_O1;
wire [0:0] reg_P_inst0_out;
TestInitClockArg_comb TestInitClockArg_comb_inst0 (
    .CLK(CLK),
    .self_x_O(reg_P_inst0_out),
    .O0(TestInitClockArg_comb_inst0_O0),
    .O1(TestInitClockArg_comb_inst0_O1)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P_inst0 (
    .clk(CLK2),
    .in(TestInitClockArg_comb_inst0_O0),
    .out(reg_P_inst0_out)
);
assign O = TestInitClockArg_comb_inst0_O1;
endmodule


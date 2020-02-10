module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module DualClockRAM (
    input [7:0] RADDR,
    input [7:0] WADDR,
    input [7:0] WDATA,
    output [7:0] RDATA,
    input WE,
    input RCLK,
    input WCLK
);
wire [7:0] const_0_8_out;
coreir_const #(
    .value(8'h00),
    .width(8)
) const_0_8 (
    .out(const_0_8_out)
);
assign RDATA = const_0_8_out;
endmodule

module TestDualClockRAM_comb (
    input [7:0] ADDR,
    input [7:0] WDATA,
    input WE,
    input RCLK,
    input WCLK,
    output [7:0] O
);
wire [7:0] DualClockRAM_inst0_RDATA;
DualClockRAM DualClockRAM_inst0 (
    .RADDR(ADDR),
    .WADDR(ADDR),
    .WDATA(WDATA),
    .RDATA(DualClockRAM_inst0_RDATA),
    .WE(WE),
    .RCLK(RCLK),
    .WCLK(WCLK)
);
assign O = DualClockRAM_inst0_RDATA;
endmodule

module TestDualClockRAM (
    input [7:0] ADDR,
    input [7:0] WDATA,
    input WE,
    input RCLK,
    input WCLK,
    output [7:0] O
);
wire [7:0] TestDualClockRAM_comb_inst0_O;
TestDualClockRAM_comb TestDualClockRAM_comb_inst0 (
    .ADDR(ADDR),
    .WDATA(WDATA),
    .WE(WE),
    .RCLK(RCLK),
    .WCLK(WCLK),
    .O(TestDualClockRAM_comb_inst0_O)
);
assign O = TestDualClockRAM_comb_inst0_O;
endmodule


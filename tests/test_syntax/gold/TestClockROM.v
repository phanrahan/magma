module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module ROM (
    input [7:0] RADDR,
    output [7:0] RDATA,
    input RCLK
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

module TestClockROM_comb (
    input [7:0] ADDR,
    input RCLK,
    output [7:0] O
);
wire [7:0] ROM_inst0_RDATA;
ROM ROM_inst0 (
    .RADDR(ADDR),
    .RDATA(ROM_inst0_RDATA),
    .RCLK(RCLK)
);
assign O = ROM_inst0_RDATA;
endmodule

module TestClockROM (
    input [7:0] ADDR,
    input RCLK,
    output [7:0] O
);
wire [7:0] TestClockROM_comb_inst0_O;
TestClockROM_comb TestClockROM_comb_inst0 (
    .ADDR(ADDR),
    .RCLK(RCLK),
    .O(TestClockROM_comb_inst0_O)
);
assign O = TestClockROM_comb_inst0_O;
endmodule


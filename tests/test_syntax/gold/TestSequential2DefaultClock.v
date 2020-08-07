module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
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

module DefaultClock (
    output [7:0] O,
    input CLK
);
wire [7:0] DualClockRAM_inst0_RADDR;
wire [7:0] DualClockRAM_inst0_WADDR;
wire [7:0] DualClockRAM_inst0_WDATA;
wire [7:0] DualClockRAM_inst0_RDATA;
wire DualClockRAM_inst0_WE;
wire DualClockRAM_inst0_RCLK;
wire DualClockRAM_inst0_WCLK;
wire bit_const_0_None_out;
wire [7:0] const_0_8_out;
assign DualClockRAM_inst0_RADDR = const_0_8_out;
assign DualClockRAM_inst0_WADDR = const_0_8_out;
assign DualClockRAM_inst0_WDATA = const_0_8_out;
assign DualClockRAM_inst0_WE = bit_const_0_None_out;
assign DualClockRAM_inst0_RCLK = CLK;
assign DualClockRAM_inst0_WCLK = CLK;
DualClockRAM DualClockRAM_inst0 (
    .RADDR(DualClockRAM_inst0_RADDR),
    .WADDR(DualClockRAM_inst0_WADDR),
    .WDATA(DualClockRAM_inst0_WDATA),
    .RDATA(DualClockRAM_inst0_RDATA),
    .WE(DualClockRAM_inst0_WE),
    .RCLK(DualClockRAM_inst0_RCLK),
    .WCLK(DualClockRAM_inst0_WCLK)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(8'h00),
    .width(8)
) const_0_8 (
    .out(const_0_8_out)
);
assign O = DualClockRAM_inst0_RDATA;
endmodule


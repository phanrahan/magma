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
wire [7:0] DualClockRAM_inst0_RDATA;
wire bit_const_0_None_out;
wire [7:0] const_0_8_out;
DualClockRAM DualClockRAM_inst0 (
    .RADDR(const_0_8_out),
    .WADDR(const_0_8_out),
    .WDATA(const_0_8_out),
    .RDATA(DualClockRAM_inst0_RDATA),
    .WE(bit_const_0_None_out),
    .RCLK(CLK),
    .WCLK(CLK)
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


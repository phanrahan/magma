module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

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
wire [7:0] Const_inst0_out;
coreir_const #(
    .value(8'h00),
    .width(8)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_term #(
    .width(8)
) term_inst0 (
    .in(Const_inst0_out)
);
assign RDATA = Const_inst0_out;
endmodule

module ExplicitClock (
    input WCLK,
    input RCLK,
    output [7:0] O,
    input CLK
);
wire [7:0] Const_inst0_out;
wire [7:0] Const_inst1_out;
wire [7:0] Const_inst2_out;
wire [7:0] DualClockRAM_inst0_RDATA;
wire bit_const_0_None_out;
coreir_const #(
    .value(8'h00),
    .width(8)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_const #(
    .value(8'h00),
    .width(8)
) Const_inst1 (
    .out(Const_inst1_out)
);
coreir_const #(
    .value(8'h00),
    .width(8)
) Const_inst2 (
    .out(Const_inst2_out)
);
DualClockRAM DualClockRAM_inst0 (
    .RADDR(Const_inst0_out),
    .WADDR(Const_inst1_out),
    .WDATA(Const_inst2_out),
    .RDATA(DualClockRAM_inst0_RDATA),
    .WE(bit_const_0_None_out),
    .RCLK(RCLK),
    .WCLK(WCLK)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_term #(
    .width(8)
) term_inst0 (
    .in(Const_inst0_out)
);
coreir_term #(
    .width(8)
) term_inst1 (
    .in(Const_inst1_out)
);
coreir_term #(
    .width(8)
) term_inst2 (
    .in(Const_inst2_out)
);
assign O = DualClockRAM_inst0_RDATA;
endmodule


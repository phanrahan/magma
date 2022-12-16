module coreir_sync_read_mem #(
    parameter has_init = 1'b0,
    parameter depth = 1,
    parameter width = 1,
    parameter [(width * depth) - 1:0] init = 0
) (
    input clk,
    input [width-1:0] wdata,
    input [$clog2(depth)-1:0] waddr,
    input wen,
    output [width-1:0] rdata,
    input [$clog2(depth)-1:0] raddr,
    input ren
);
  reg [width-1:0] data [depth-1:0];
  generate if (has_init) begin
    genvar j;
    for (j = 0; j < depth; j = j + 1) begin
      initial begin
        data[j] = init[(j+1)*width-1:j*width];
      end
    end
  end
  endgenerate
  always @(posedge clk) begin
    if (wen) begin
      data[waddr] <= wdata;
    end
  end
  reg [width-1:0] rdata_reg;
  always @(posedge clk) begin
    if (ren) rdata_reg <= data[raddr];
  end
  assign rdata = rdata_reg;

endmodule

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

module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module commonlib_muxn__N2__width5 (
    input [4:0] in_data [1:0],
    input [0:0] in_sel,
    output [4:0] out
);
wire [4:0] _join_out;
coreir_mux #(
    .width(5)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xBits5 (
    input [4:0] I0,
    input [4:0] I1,
    input S,
    output [4:0] O
);
wire [4:0] mux_out;
wire [4:0] mux_in_data [1:0];
assign mux_in_data[1] = I1;
assign mux_in_data[0] = I0;
commonlib_muxn__N2__width5 mux (
    .in_data(mux_in_data),
    .in_sel(S),
    .out(mux_out)
);
assign O = mux_out;
endmodule

module Register (
    input [4:0] I,
    output [4:0] O,
    input CE,
    input CLK
);
wire [4:0] _reg_out;
wire [4:0] enable_mux_O;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(5'h00),
    .width(5)
) _reg (
    .clk(CLK),
    .in(enable_mux_O),
    .out(_reg_out)
);
Mux2xBits5 enable_mux (
    .I0(_reg_out),
    .I1(I),
    .S(CE),
    .O(enable_mux_O)
);
assign O = _reg_out;
endmodule

module Memory (
    input [1:0] RADDR,
    output [4:0] RDATA,
    input CLK,
    input RE,
    input [1:0] WADDR,
    input [4:0] WDATA,
    input WE
);
wire [4:0] Register_inst0_O;
wire [4:0] coreir_mem_rdata;
Register Register_inst0 (
    .I(coreir_mem_rdata),
    .O(Register_inst0_O),
    .CE(RE),
    .CLK(CLK)
);
coreir_sync_read_mem #(
    .depth(4),
    .has_init(1'b0),
    .width(5)
) coreir_mem (
    .clk(CLK),
    .wdata(WDATA),
    .waddr(WADDR),
    .wen(WE),
    .rdata(coreir_mem_rdata),
    .ren(RE),
    .raddr(RADDR)
);
assign RDATA = Register_inst0_O;
endmodule

module test_memory_read_latency_True (
    input [1:0] raddr,
    output [4:0] rdata,
    input [1:0] waddr,
    input [4:0] wdata,
    input clk,
    input wen,
    input ren
);
wire [4:0] Memory_inst0_RDATA;
Memory Memory_inst0 (
    .RADDR(raddr),
    .RDATA(Memory_inst0_RDATA),
    .CLK(clk),
    .RE(ren),
    .WADDR(waddr),
    .WDATA(wdata),
    .WE(wen)
);
assign rdata = Memory_inst0_RDATA;
endmodule


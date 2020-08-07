module coreir_mem #(
    parameter has_init = 1'b0,
    parameter sync_read = 1'b0,
    parameter depth = 1,
    parameter width = 1
) (
    input clk,
    input [width-1:0] wdata,
    input [$clog2(depth)-1:0] waddr,
    input wen,
    output [width-1:0] rdata,
    input [$clog2(depth)-1:0] raddr
);
  reg [width-1:0] data [depth-1:0];
  parameter [width*depth-1:0] init = 0;
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
  generate if (sync_read) begin
  reg [width-1:0] rdata_reg;
  always @(posedge clk) begin
    rdata_reg <= data[raddr];
  end
  assign rdata = rdata_reg;
  end else begin
  assign rdata = data[raddr];
  end
  endgenerate

endmodule

module Memory (
    input [1:0] RADDR,
    output [4:0] RDATA,
    input CLK,
    input [1:0] WADDR,
    input [4:0] WDATA,
    input WE
);
wire coreir_mem4x5_inst0_clk;
wire [4:0] coreir_mem4x5_inst0_wdata;
wire [1:0] coreir_mem4x5_inst0_waddr;
wire coreir_mem4x5_inst0_wen;
wire [4:0] coreir_mem4x5_inst0_rdata;
wire [1:0] coreir_mem4x5_inst0_raddr;
assign coreir_mem4x5_inst0_clk = CLK;
assign coreir_mem4x5_inst0_wdata = WDATA;
assign coreir_mem4x5_inst0_waddr = WADDR;
assign coreir_mem4x5_inst0_wen = WE;
assign coreir_mem4x5_inst0_raddr = RADDR;
coreir_mem #(
    .depth(4),
    .has_init(1'b0),
    .sync_read(1'b0),
    .width(5)
) coreir_mem4x5_inst0 (
    .clk(coreir_mem4x5_inst0_clk),
    .wdata(coreir_mem4x5_inst0_wdata),
    .waddr(coreir_mem4x5_inst0_waddr),
    .wen(coreir_mem4x5_inst0_wen),
    .rdata(coreir_mem4x5_inst0_rdata),
    .raddr(coreir_mem4x5_inst0_raddr)
);
assign RDATA = coreir_mem4x5_inst0_rdata;
endmodule

module test_memory_basic (
    input [1:0] raddr,
    output [4:0] rdata,
    input [1:0] waddr,
    input [4:0] wdata,
    input clk,
    input wen
);
wire [1:0] Memory_inst0_RADDR;
wire [4:0] Memory_inst0_RDATA;
wire Memory_inst0_CLK;
wire [1:0] Memory_inst0_WADDR;
wire [4:0] Memory_inst0_WDATA;
wire Memory_inst0_WE;
assign Memory_inst0_RADDR = raddr;
assign Memory_inst0_CLK = clk;
assign Memory_inst0_WADDR = waddr;
assign Memory_inst0_WDATA = wdata;
assign Memory_inst0_WE = wen;
Memory Memory_inst0 (
    .RADDR(Memory_inst0_RADDR),
    .RDATA(Memory_inst0_RDATA),
    .CLK(Memory_inst0_CLK),
    .WADDR(Memory_inst0_WADDR),
    .WDATA(Memory_inst0_WDATA),
    .WE(Memory_inst0_WE)
);
assign rdata = Memory_inst0_RDATA;
endmodule


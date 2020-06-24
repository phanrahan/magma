module coreir_mem #(
    parameter has_init = 1'b0,
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
  assign rdata = data[raddr];
endmodule

module Memory (
    input [1:0] RADDR,
    output [4:0] RDATA,
    input CLK,
    input [1:0] WADDR,
    input [4:0] WDATA,
    input WE
);
wire [4:0] coreir_mem4x5_inst0_rdata;
coreir_mem #(
    .depth(4),
    .has_init(1'b0),
    .width(5)
) coreir_mem4x5_inst0 (
    .clk(CLK),
    .wdata(WDATA),
    .waddr(WADDR),
    .wen(WE),
    .rdata(coreir_mem4x5_inst0_rdata),
    .raddr(RADDR)
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
wire [4:0] Memory_inst0_RDATA;
Memory Memory_inst0 (
    .RADDR(raddr),
    .RDATA(Memory_inst0_RDATA),
    .CLK(clk),
    .WADDR(waddr),
    .WDATA(wdata),
    .WE(wen)
);
assign rdata = Memory_inst0_RDATA;
endmodule


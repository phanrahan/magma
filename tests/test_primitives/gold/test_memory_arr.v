module coreir_mem #(
    parameter has_init = 1'b0,
    parameter sync_read = 1'b0,
    parameter depth = 1,
    parameter width = 1,
    parameter [(width * depth) - 1:0] init = 0
) (
    input clk,
    input [width-1:0] wdata,
    input [$clog2(depth)-1:0] waddr,
    input wen,
    output [width-1:0] rdata,
    input [$clog2(depth)-1:0] raddr
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
    input CLK,
    input [1:0] RADDR,
    output RDATA_0_X,
    output [4:0] RDATA_0_Y,
    output RDATA_1_X,
    output [4:0] RDATA_1_Y,
    input [1:0] WADDR,
    input WDATA_0_X,
    input [4:0] WDATA_0_Y,
    input WDATA_1_X,
    input [4:0] WDATA_1_Y,
    input WE
);
wire [11:0] coreir_mem4x12_inst0_rdata;
wire [11:0] coreir_mem4x12_inst0_wdata;
assign coreir_mem4x12_inst0_wdata = {WDATA_1_Y,WDATA_1_X,WDATA_0_Y,WDATA_0_X};
coreir_mem #(
    .depth(4),
    .has_init(1'b0),
    .sync_read(1'b0),
    .width(12)
) coreir_mem4x12_inst0 (
    .clk(CLK),
    .wdata(coreir_mem4x12_inst0_wdata),
    .waddr(WADDR),
    .wen(WE),
    .rdata(coreir_mem4x12_inst0_rdata),
    .raddr(RADDR)
);
assign RDATA_0_X = coreir_mem4x12_inst0_rdata[0];
assign RDATA_0_Y = {coreir_mem4x12_inst0_rdata[5],coreir_mem4x12_inst0_rdata[4],coreir_mem4x12_inst0_rdata[3],coreir_mem4x12_inst0_rdata[2],coreir_mem4x12_inst0_rdata[1]};
assign RDATA_1_X = coreir_mem4x12_inst0_rdata[6];
assign RDATA_1_Y = {coreir_mem4x12_inst0_rdata[11],coreir_mem4x12_inst0_rdata[10],coreir_mem4x12_inst0_rdata[9],coreir_mem4x12_inst0_rdata[8],coreir_mem4x12_inst0_rdata[7]};
endmodule

module test_memory_arr (
    input clk,
    input [1:0] raddr,
    output rdata_0_X,
    output [4:0] rdata_0_Y,
    output rdata_1_X,
    output [4:0] rdata_1_Y,
    input [1:0] waddr,
    input wdata_0_X,
    input [4:0] wdata_0_Y,
    input wdata_1_X,
    input [4:0] wdata_1_Y,
    input wen
);
Memory Memory_inst0 (
    .CLK(clk),
    .RADDR(raddr),
    .RDATA_0_X(rdata_0_X),
    .RDATA_0_Y(rdata_0_Y),
    .RDATA_1_X(rdata_1_X),
    .RDATA_1_Y(rdata_1_Y),
    .WADDR(waddr),
    .WDATA_0_X(wdata_0_X),
    .WDATA_0_Y(wdata_0_Y),
    .WDATA_1_X(wdata_1_X),
    .WDATA_1_Y(wdata_1_Y),
    .WE(1'b1)
);
endmodule


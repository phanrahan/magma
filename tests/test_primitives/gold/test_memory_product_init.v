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
    output [7:0] RDATA_X,
    output [7:0] RDATA_Y
);
wire [15:0] coreir_mem4x16_inst0_rdata;
coreir_mem #(
    .init({16'd127,16'd65535,16'd32640,16'd32768}),
    .depth(4),
    .has_init(1'b1),
    .sync_read(1'b0),
    .width(16)
) coreir_mem4x16_inst0 (
    .clk(CLK),
    .wdata(16'h0000),
    .waddr(2'h0),
    .wen(1'b0),
    .rdata(coreir_mem4x16_inst0_rdata),
    .raddr(RADDR)
);
assign RDATA_X = {coreir_mem4x16_inst0_rdata[7],coreir_mem4x16_inst0_rdata[6],coreir_mem4x16_inst0_rdata[5],coreir_mem4x16_inst0_rdata[4],coreir_mem4x16_inst0_rdata[3],coreir_mem4x16_inst0_rdata[2],coreir_mem4x16_inst0_rdata[1],coreir_mem4x16_inst0_rdata[0]};
assign RDATA_Y = {coreir_mem4x16_inst0_rdata[15],coreir_mem4x16_inst0_rdata[14],coreir_mem4x16_inst0_rdata[13],coreir_mem4x16_inst0_rdata[12],coreir_mem4x16_inst0_rdata[11],coreir_mem4x16_inst0_rdata[10],coreir_mem4x16_inst0_rdata[9],coreir_mem4x16_inst0_rdata[8]};
endmodule

module test_memory_product_init (
    input clk,
    input [1:0] raddr,
    output [7:0] rdata_X,
    output [7:0] rdata_Y
);
Memory Memory_inst0 (
    .CLK(clk),
    .RADDR(raddr),
    .RDATA_X(rdata_X),
    .RDATA_Y(rdata_Y)
);
endmodule


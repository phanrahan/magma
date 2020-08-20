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

module Memory (
    input [1:0] RADDR,
    output [4:0] RDATA,
    input CLK
);
wire bit_const_0_None_out;
wire [1:0] const_0_2_out;
wire [4:0] const_0_5_out;
wire [4:0] coreir_mem4x5_inst0_rdata;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(2'h0),
    .width(2)
) const_0_2 (
    .out(const_0_2_out)
);
coreir_const #(
    .value(5'h00),
    .width(5)
) const_0_5 (
    .out(const_0_5_out)
);
coreir_mem #(
    .init({5'd0,5'd19,5'd10,5'd7}),
    .depth(4),
    .has_init(1'b1),
    .sync_read(1'b0),
    .width(5)
) coreir_mem4x5_inst0 (
    .clk(CLK),
    .wdata(const_0_5_out),
    .waddr(const_0_2_out),
    .wen(bit_const_0_None_out),
    .rdata(coreir_mem4x5_inst0_rdata),
    .raddr(RADDR)
);
assign RDATA = coreir_mem4x5_inst0_rdata;
endmodule

module test_memory_read_only (
    input [1:0] raddr,
    output [4:0] rdata,
    input clk
);
wire [4:0] Memory_inst0_RDATA;
Memory Memory_inst0 (
    .RADDR(raddr),
    .RDATA(Memory_inst0_RDATA),
    .CLK(clk)
);
assign rdata = Memory_inst0_RDATA;
endmodule


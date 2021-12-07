module mantle_wire__typeBitIn8 (
    output [7:0] in,
    input [7:0] out
);
assign in = out;
endmodule

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
    input CLK,
    input [1:0] RADDR,
    output [7:0] RDATA_X,
    output [7:0] RDATA_Y
);
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire [1:0] const_0_2_out;
wire [15:0] coreir_mem4x16_inst0_rdata;
wire [7:0] self_RDATA_X_in;
wire [7:0] self_RDATA_Y_in;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(16'h0000),
    .width(16)
) const_0_16 (
    .out(const_0_16_out)
);
coreir_const #(
    .value(2'h0),
    .width(2)
) const_0_2 (
    .out(const_0_2_out)
);
coreir_mem #(
    .init({16'd127,16'd65535,16'd32640,16'd32768}),
    .depth(4),
    .has_init(1'b1),
    .sync_read(1'b0),
    .width(16)
) coreir_mem4x16_inst0 (
    .clk(CLK),
    .wdata(const_0_16_out),
    .waddr(const_0_2_out),
    .wen(bit_const_0_None_out),
    .rdata(coreir_mem4x16_inst0_rdata),
    .raddr(RADDR)
);
mantle_wire__typeBitIn8 self_RDATA_X (
    .in(self_RDATA_X_in),
    .out(coreir_mem4x16_inst0_rdata[7:0])
);
mantle_wire__typeBitIn8 self_RDATA_Y (
    .in(self_RDATA_Y_in),
    .out(coreir_mem4x16_inst0_rdata[15:8])
);
assign RDATA_X = self_RDATA_X_in;
assign RDATA_Y = self_RDATA_Y_in;
endmodule

module test_memory_product_init (
    input clk,
    input [1:0] raddr,
    output [7:0] rdata_X,
    output [7:0] rdata_Y
);
wire [7:0] Memory_inst0_RDATA_X;
wire [7:0] Memory_inst0_RDATA_Y;
Memory Memory_inst0 (
    .CLK(clk),
    .RADDR(raddr),
    .RDATA_X(Memory_inst0_RDATA_X),
    .RDATA_Y(Memory_inst0_RDATA_Y)
);
assign rdata_X = Memory_inst0_RDATA_X;
assign rdata_Y = Memory_inst0_RDATA_Y;
endmodule


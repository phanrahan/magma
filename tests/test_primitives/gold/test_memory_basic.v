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
    input CLK,
    input [1:0] WADDR,
    input [4:0] WDATA,
    input WE
);
wire [4:0] coreir_mem4x5_inst0_rdata;
coreir_mem #(
    .depth(4),
    .has_init(1'b0),
    .sync_read(1'b0),
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

module ConditionalDriversImpl (
    input C0,
    input [1:0] C0I0,
    input [4:0] C0I1,
    input C0I2,
    output [1:0] O0,
    output [4:0] O1,
    output O2
);
reg [1:0] O0_reg;
reg [4:0] O1_reg;
reg  O2_reg;
always @(*) begin
    O0_reg = 0;
    O1_reg = 0;
    O2_reg = 0;
    if (C0) begin
        O0_reg = C0I0;
        O1_reg = C0I1;
        O2_reg = C0I2;
    end
end
assign O0 = O0_reg;
assign O1 = O1_reg;
assign O2 = O2_reg;

endmodule

module test_memory_basic (
    input [1:0] raddr,
    output [4:0] rdata,
    input [1:0] waddr,
    input [4:0] wdata,
    input clk,
    input wen
);
wire [1:0] ConditionalDriversImpl_inst0_O0;
wire [4:0] ConditionalDriversImpl_inst0_O1;
wire ConditionalDriversImpl_inst0_O2;
wire [4:0] Memory_inst0_RDATA;
wire bit_const_1_None_out;
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(wen),
    .C0I0(waddr),
    .C0I1(wdata),
    .C0I2(bit_const_1_None_out),
    .O0(ConditionalDriversImpl_inst0_O0),
    .O1(ConditionalDriversImpl_inst0_O1),
    .O2(ConditionalDriversImpl_inst0_O2)
);
Memory Memory_inst0 (
    .RADDR(raddr),
    .RDATA(Memory_inst0_RDATA),
    .CLK(clk),
    .WADDR(ConditionalDriversImpl_inst0_O0),
    .WDATA(ConditionalDriversImpl_inst0_O1),
    .WE(ConditionalDriversImpl_inst0_O2)
);
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
assign rdata = Memory_inst0_RDATA;
endmodule


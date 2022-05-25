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
    input [4:0] RADDR,
    output [7:0] RDATA,
    input CLK,
    input [4:0] WADDR,
    input [7:0] WDATA,
    input WE
);
coreir_mem #(
    .depth(32),
    .has_init(1'b0),
    .sync_read(1'b0),
    .width(8)
) coreir_mem32x8_inst0 (
    .clk(CLK),
    .wdata(WDATA),
    .waddr(WADDR),
    .wen(WE),
    .rdata(RDATA),
    .raddr(RADDR)
);
endmodule

module ConditionalDriversImpl (
    input C0,
    input [4:0] C0I0,
    input [7:0] C0I1,
    input C0I2,
    input [4:0] C0I3,
    input [7:0] C0I4,
    input C1,
    input [4:0] C1I0,
    input [7:0] C1I1,
    input C1I2,
    input [4:0] C1I3,
    input [7:0] C1I4,
    output [4:0] O0,
    output [4:0] O1,
    output [7:0] O2,
    output O3,
    output [7:0] O4
);
reg [4:0] O0_reg;
reg [4:0] O1_reg;
reg [7:0] O2_reg;
reg  O3_reg;
reg [7:0] O4_reg;
always @(*) begin
    O0_reg = 0;
    O1_reg = 0;
    O2_reg = 0;
    O3_reg = 0;
    if (C0) begin
        O1_reg = C0I3;
        O2_reg = C0I1;
        O3_reg = C1I2;
        O0_reg = C0I3;
        O4_reg = C1I4;
    end else begin
        if (C1) begin
            O1_reg = C1I3;
            O2_reg = C1I1;
            O3_reg = C1I2;
            O0_reg = C1I3;
            O4_reg = C1I4;
        end
    end
end
assign O0 = O0_reg;
assign O1 = O1_reg;
assign O2 = O2_reg;
assign O3 = O3_reg;
assign O4 = O4_reg;

endmodule

module Foo (
    input [7:0] data0,
    input [4:0] addr0,
    input en0,
    input [7:0] data1,
    input [4:0] addr1,
    input en1,
    output [7:0] out,
    input CLK
);
wire [4:0] ConditionalDriversImpl_inst0_O0;
wire [4:0] ConditionalDriversImpl_inst0_O1;
wire [7:0] ConditionalDriversImpl_inst0_O2;
wire ConditionalDriversImpl_inst0_O3;
wire [7:0] Memory_inst0_RDATA;
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(en0),
    .C0I0(addr0),
    .C0I1(data0),
    .C0I2(1'b1),
    .C0I3(addr0),
    .C0I4(Memory_inst0_RDATA),
    .C1(en1),
    .C1I0(addr1),
    .C1I1(data1),
    .C1I2(1'b1),
    .C1I3(addr1),
    .C1I4(Memory_inst0_RDATA),
    .O0(ConditionalDriversImpl_inst0_O0),
    .O1(ConditionalDriversImpl_inst0_O1),
    .O2(ConditionalDriversImpl_inst0_O2),
    .O3(ConditionalDriversImpl_inst0_O3),
    .O4(out)
);
Memory Memory_inst0 (
    .RADDR(ConditionalDriversImpl_inst0_O0),
    .RDATA(Memory_inst0_RDATA),
    .CLK(CLK),
    .WADDR(ConditionalDriversImpl_inst0_O1),
    .WDATA(ConditionalDriversImpl_inst0_O2),
    .WE(ConditionalDriversImpl_inst0_O3)
);
endmodule


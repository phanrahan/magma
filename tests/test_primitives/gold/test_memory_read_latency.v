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

module Register (
    input [4:0] I,
    output [4:0] O,
    input CLK
);
wire [4:0] reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(5'h00),
    .width(5)
) reg_P_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P_inst0_out)
);
assign O = reg_P_inst0_out;
endmodule

module Memory (
    input [1:0] RADDR,
    output [4:0] RDATA,
    input CLK,
    input [1:0] WADDR,
    input [4:0] WDATA,
    input WE
);
wire [4:0] Register_inst0_O;
wire [4:0] Register_inst1_O;
wire [4:0] coreir_mem4x5_inst0_rdata;
Register Register_inst0 (
    .I(coreir_mem4x5_inst0_rdata),
    .O(Register_inst0_O),
    .CLK(CLK)
);
Register Register_inst1 (
    .I(Register_inst0_O),
    .O(Register_inst1_O),
    .CLK(CLK)
);
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
assign RDATA = Register_inst1_O;
endmodule

module test_memory_read_latency (
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


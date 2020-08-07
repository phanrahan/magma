module mantle_wire__typeBitIn5 (
    output [4:0] in,
    input [4:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit5 (
    input [4:0] in,
    output [4:0] out
);
assign out = in;
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
wire [4:0] _$_U1_in;
wire [4:0] _$_U1_out;
wire [4:0] _$_U2_in;
wire [4:0] _$_U2_out;
wire [4:0] _$_U3_in;
wire [4:0] _$_U3_out;
wire [4:0] _$_U4_in;
wire [4:0] _$_U4_out;
wire coreir_mem4x12_inst0_clk;
wire [11:0] coreir_mem4x12_inst0_wdata;
wire [1:0] coreir_mem4x12_inst0_waddr;
wire coreir_mem4x12_inst0_wen;
wire [11:0] coreir_mem4x12_inst0_rdata;
wire [1:0] coreir_mem4x12_inst0_raddr;
assign _$_U1_out = coreir_mem4x12_inst0_rdata[5:1];
mantle_wire__typeBitIn5 _$_U1 (
    .in(_$_U1_in),
    .out(_$_U1_out)
);
assign _$_U2_out = coreir_mem4x12_inst0_rdata[11:7];
mantle_wire__typeBitIn5 _$_U2 (
    .in(_$_U2_in),
    .out(_$_U2_out)
);
assign _$_U3_in = WDATA_0_Y;
mantle_wire__typeBit5 _$_U3 (
    .in(_$_U3_in),
    .out(_$_U3_out)
);
assign _$_U4_in = WDATA_1_Y;
mantle_wire__typeBit5 _$_U4 (
    .in(_$_U4_in),
    .out(_$_U4_out)
);
assign coreir_mem4x12_inst0_clk = CLK;
assign coreir_mem4x12_inst0_wdata = {_$_U4_out[4:0],WDATA_1_X,_$_U3_out[4:0],WDATA_0_X};
assign coreir_mem4x12_inst0_waddr = WADDR;
assign coreir_mem4x12_inst0_wen = WE;
assign coreir_mem4x12_inst0_raddr = RADDR;
coreir_mem #(
    .depth(4),
    .has_init(1'b0),
    .sync_read(1'b0),
    .width(12)
) coreir_mem4x12_inst0 (
    .clk(coreir_mem4x12_inst0_clk),
    .wdata(coreir_mem4x12_inst0_wdata),
    .waddr(coreir_mem4x12_inst0_waddr),
    .wen(coreir_mem4x12_inst0_wen),
    .rdata(coreir_mem4x12_inst0_rdata),
    .raddr(coreir_mem4x12_inst0_raddr)
);
assign RDATA_0_X = coreir_mem4x12_inst0_rdata[0];
assign RDATA_0_Y = _$_U1_in;
assign RDATA_1_X = coreir_mem4x12_inst0_rdata[6];
assign RDATA_1_Y = _$_U2_in;
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
wire Memory_inst0_CLK;
wire [1:0] Memory_inst0_RADDR;
wire Memory_inst0_RDATA_0_X;
wire [4:0] Memory_inst0_RDATA_0_Y;
wire Memory_inst0_RDATA_1_X;
wire [4:0] Memory_inst0_RDATA_1_Y;
wire [1:0] Memory_inst0_WADDR;
wire Memory_inst0_WDATA_0_X;
wire [4:0] Memory_inst0_WDATA_0_Y;
wire Memory_inst0_WDATA_1_X;
wire [4:0] Memory_inst0_WDATA_1_Y;
wire Memory_inst0_WE;
assign Memory_inst0_CLK = clk;
assign Memory_inst0_RADDR = raddr;
assign Memory_inst0_WADDR = waddr;
assign Memory_inst0_WDATA_0_X = wdata_0_X;
assign Memory_inst0_WDATA_0_Y = wdata_0_Y;
assign Memory_inst0_WDATA_1_X = wdata_1_X;
assign Memory_inst0_WDATA_1_Y = wdata_1_Y;
assign Memory_inst0_WE = wen;
Memory Memory_inst0 (
    .CLK(Memory_inst0_CLK),
    .RADDR(Memory_inst0_RADDR),
    .RDATA_0_X(Memory_inst0_RDATA_0_X),
    .RDATA_0_Y(Memory_inst0_RDATA_0_Y),
    .RDATA_1_X(Memory_inst0_RDATA_1_X),
    .RDATA_1_Y(Memory_inst0_RDATA_1_Y),
    .WADDR(Memory_inst0_WADDR),
    .WDATA_0_X(Memory_inst0_WDATA_0_X),
    .WDATA_0_Y(Memory_inst0_WDATA_0_Y),
    .WDATA_1_X(Memory_inst0_WDATA_1_X),
    .WDATA_1_Y(Memory_inst0_WDATA_1_Y),
    .WE(Memory_inst0_WE)
);
assign rdata_0_X = Memory_inst0_RDATA_0_X;
assign rdata_0_Y = Memory_inst0_RDATA_0_Y;
assign rdata_1_X = Memory_inst0_RDATA_1_X;
assign rdata_1_Y = Memory_inst0_RDATA_1_Y;
endmodule


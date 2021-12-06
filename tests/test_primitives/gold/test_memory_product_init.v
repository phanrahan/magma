module mantle_wire__typeBitIn8 (
    output [7:0] in,
    input [7:0] out
);
assign in = out;
endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

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
wire [1:0] Const_inst0_out;
wire [15:0] Const_inst1_out;
wire bit_const_0_None_out;
wire [15:0] coreir_mem4x16_inst0_rdata;
wire [7:0] self_RDATA_X_in;
wire [7:0] self_RDATA_Y_in;
coreir_const #(
    .value(2'h0),
    .width(2)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_const #(
    .value(16'h0000),
    .width(16)
) Const_inst1 (
    .out(Const_inst1_out)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_mem #(
    .init({16'd127,16'd65535,16'd32640,16'd32768}),
    .depth(4),
    .has_init(1'b1),
    .sync_read(1'b0),
    .width(16)
) coreir_mem4x16_inst0 (
    .clk(CLK),
    .wdata(Const_inst1_out),
    .waddr(Const_inst0_out),
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
coreir_term #(
    .width(2)
) term_inst0 (
    .in(Const_inst0_out)
);
coreir_term #(
    .width(16)
) term_inst1 (
    .in(Const_inst1_out)
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
wire [7:0] Const_inst0_out;
wire [7:0] Const_inst1_out;
wire [7:0] Const_inst2_out;
wire [7:0] Const_inst3_out;
wire [7:0] Const_inst4_out;
wire [7:0] Const_inst5_out;
wire [7:0] Const_inst6_out;
wire [7:0] Const_inst7_out;
wire [7:0] Memory_inst0_RDATA_X;
wire [7:0] Memory_inst0_RDATA_Y;
coreir_const #(
    .value(8'h00),
    .width(8)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_const #(
    .value(8'h80),
    .width(8)
) Const_inst1 (
    .out(Const_inst1_out)
);
coreir_const #(
    .value(8'h80),
    .width(8)
) Const_inst2 (
    .out(Const_inst2_out)
);
coreir_const #(
    .value(8'h7f),
    .width(8)
) Const_inst3 (
    .out(Const_inst3_out)
);
coreir_const #(
    .value(8'hff),
    .width(8)
) Const_inst4 (
    .out(Const_inst4_out)
);
coreir_const #(
    .value(8'hff),
    .width(8)
) Const_inst5 (
    .out(Const_inst5_out)
);
coreir_const #(
    .value(8'h7f),
    .width(8)
) Const_inst6 (
    .out(Const_inst6_out)
);
coreir_const #(
    .value(8'h00),
    .width(8)
) Const_inst7 (
    .out(Const_inst7_out)
);
Memory Memory_inst0 (
    .CLK(clk),
    .RADDR(raddr),
    .RDATA_X(Memory_inst0_RDATA_X),
    .RDATA_Y(Memory_inst0_RDATA_Y)
);
coreir_term #(
    .width(8)
) term_inst0 (
    .in(Const_inst0_out)
);
coreir_term #(
    .width(8)
) term_inst1 (
    .in(Const_inst1_out)
);
coreir_term #(
    .width(8)
) term_inst2 (
    .in(Const_inst2_out)
);
coreir_term #(
    .width(8)
) term_inst3 (
    .in(Const_inst3_out)
);
coreir_term #(
    .width(8)
) term_inst4 (
    .in(Const_inst4_out)
);
coreir_term #(
    .width(8)
) term_inst5 (
    .in(Const_inst5_out)
);
coreir_term #(
    .width(8)
) term_inst6 (
    .in(Const_inst6_out)
);
coreir_term #(
    .width(8)
) term_inst7 (
    .in(Const_inst7_out)
);
assign rdata_X = Memory_inst0_RDATA_X;
assign rdata_Y = Memory_inst0_RDATA_Y;
endmodule


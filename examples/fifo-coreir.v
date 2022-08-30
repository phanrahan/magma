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

module RAM4x32 (
    input [1:0] RADDR,
    output [31:0] RDATA,
    input [1:0] WADDR,
    input [31:0] WDATA,
    input CLK,
    input WE
);
coreir_mem #(
    .depth(4),
    .has_init(1'b0),
    .sync_read(1'b0),
    .width(32)
) coreir_mem4x32_inst0 (
    .clk(CLK),
    .wdata(WDATA),
    .waddr(WADDR),
    .wen(WE),
    .rdata(RDATA),
    .raddr(RADDR)
);
endmodule

module Mux2xOutBits3 (
    input [2:0] I0,
    input [2:0] I1,
    input S,
    output [2:0] O
);
reg [2:0] coreir_commonlib_mux2x3_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x3_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x3_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x3_inst0_out;
endmodule

module FIFO (
    input CLK,
    input [7:0] data_in_data_exponent,
    input data_in_data_sign,
    input [22:0] data_in_data_significand,
    output data_in_ready,
    input data_in_valid,
    output [7:0] data_out_data_exponent,
    output data_out_data_sign,
    output [22:0] data_out_data_significand,
    input data_out_ready,
    output data_out_valid
);
wire [2:0] Mux2xOutBits3_inst0_O;
wire [2:0] Mux2xOutBits3_inst1_O;
wire [31:0] RAM4x32_inst0_RDATA;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire [2:0] magma_UInt_3_add_inst0_out;
wire [2:0] magma_UInt_3_add_inst1_out;
wire [2:0] reg_P_inst0_out;
wire [2:0] reg_P_inst1_out;
Mux2xOutBits3 Mux2xOutBits3_inst0 (
    .I0(reg_P_inst1_out),
    .I1(magma_UInt_3_add_inst0_out),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBits3_inst0_O)
);
Mux2xOutBits3 Mux2xOutBits3_inst1 (
    .I0(reg_P_inst0_out),
    .I1(magma_UInt_3_add_inst1_out),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xOutBits3_inst1_O)
);
wire [1:0] RAM4x32_inst0_RADDR;
assign RAM4x32_inst0_RADDR = {reg_P_inst0_out[1],reg_P_inst0_out[0]};
wire [1:0] RAM4x32_inst0_WADDR;
assign RAM4x32_inst0_WADDR = {reg_P_inst1_out[1],reg_P_inst1_out[0]};
wire [31:0] RAM4x32_inst0_WDATA;
assign RAM4x32_inst0_WDATA = {data_in_data_significand,data_in_data_exponent,data_in_data_sign};
RAM4x32 RAM4x32_inst0 (
    .RADDR(RAM4x32_inst0_RADDR),
    .RDATA(RAM4x32_inst0_RDATA),
    .WADDR(RAM4x32_inst0_WADDR),
    .WDATA(RAM4x32_inst0_WDATA),
    .CLK(CLK),
    .WE(magma_Bit_and_inst1_out)
);
assign magma_Bit_and_inst0_out = (({reg_P_inst0_out[1],reg_P_inst0_out[0]}) == ({reg_P_inst1_out[1],reg_P_inst1_out[0]})) & (reg_P_inst0_out[2] ^ reg_P_inst1_out[2]);
assign magma_Bit_and_inst1_out = data_in_valid & (~ magma_Bit_and_inst0_out);
assign magma_Bit_and_inst2_out = data_out_ready & 1'b1;
assign magma_UInt_3_add_inst0_out = 3'(reg_P_inst1_out + 3'h1);
assign magma_UInt_3_add_inst1_out = 3'(reg_P_inst0_out + 3'h1);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst0 (
    .clk(CLK),
    .in(Mux2xOutBits3_inst1_O),
    .out(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst1 (
    .clk(CLK),
    .in(Mux2xOutBits3_inst0_O),
    .out(reg_P_inst1_out)
);
assign data_in_ready = ~ magma_Bit_and_inst0_out;
assign data_out_data_exponent = {RAM4x32_inst0_RDATA[8],RAM4x32_inst0_RDATA[7],RAM4x32_inst0_RDATA[6],RAM4x32_inst0_RDATA[5],RAM4x32_inst0_RDATA[4],RAM4x32_inst0_RDATA[3],RAM4x32_inst0_RDATA[2],RAM4x32_inst0_RDATA[1]};
assign data_out_data_sign = RAM4x32_inst0_RDATA[0];
assign data_out_data_significand = {RAM4x32_inst0_RDATA[31],RAM4x32_inst0_RDATA[30],RAM4x32_inst0_RDATA[29],RAM4x32_inst0_RDATA[28],RAM4x32_inst0_RDATA[27],RAM4x32_inst0_RDATA[26],RAM4x32_inst0_RDATA[25],RAM4x32_inst0_RDATA[24],RAM4x32_inst0_RDATA[23],RAM4x32_inst0_RDATA[22],RAM4x32_inst0_RDATA[21],RAM4x32_inst0_RDATA[20],RAM4x32_inst0_RDATA[19],RAM4x32_inst0_RDATA[18],RAM4x32_inst0_RDATA[17],RAM4x32_inst0_RDATA[16],RAM4x32_inst0_RDATA[15],RAM4x32_inst0_RDATA[14],RAM4x32_inst0_RDATA[13],RAM4x32_inst0_RDATA[12],RAM4x32_inst0_RDATA[11],RAM4x32_inst0_RDATA[10],RAM4x32_inst0_RDATA[9]};
assign data_out_valid = magma_Bit_and_inst2_out;
endmodule


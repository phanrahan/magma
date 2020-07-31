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

module Register (
    input CLK,
    input [1:0] I_0_0_0,
    input [1:0] I_0_0_1,
    input [1:0] I_0_0_2,
    input [1:0] I_0_1_0,
    input [1:0] I_0_1_1,
    input [1:0] I_0_1_2,
    input [1:0] I_1_0_0,
    input [1:0] I_1_0_1,
    input [1:0] I_1_0_2,
    input [1:0] I_1_1_0,
    input [1:0] I_1_1_1,
    input [1:0] I_1_1_2,
    input [1:0] I_2_0_0,
    input [1:0] I_2_0_1,
    input [1:0] I_2_0_2,
    input [1:0] I_2_1_0,
    input [1:0] I_2_1_1,
    input [1:0] I_2_1_2,
    input [1:0] I_3_0_0,
    input [1:0] I_3_0_1,
    input [1:0] I_3_0_2,
    input [1:0] I_3_1_0,
    input [1:0] I_3_1_1,
    input [1:0] I_3_1_2,
    output [1:0] O_0_0_0,
    output [1:0] O_0_0_1,
    output [1:0] O_0_0_2,
    output [1:0] O_0_1_0,
    output [1:0] O_0_1_1,
    output [1:0] O_0_1_2,
    output [1:0] O_1_0_0,
    output [1:0] O_1_0_1,
    output [1:0] O_1_0_2,
    output [1:0] O_1_1_0,
    output [1:0] O_1_1_1,
    output [1:0] O_1_1_2,
    output [1:0] O_2_0_0,
    output [1:0] O_2_0_1,
    output [1:0] O_2_0_2,
    output [1:0] O_2_1_0,
    output [1:0] O_2_1_1,
    output [1:0] O_2_1_2,
    output [1:0] O_3_0_0,
    output [1:0] O_3_0_1,
    output [1:0] O_3_0_2,
    output [1:0] O_3_1_0,
    output [1:0] O_3_1_1,
    output [1:0] O_3_1_2
);
wire [47:0] reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(48'h000000000000),
    .width(48)
) reg_P_inst0 (
    .clk(CLK),
    .in({I_3_1_2[1:0],I_3_1_1[1:0],I_3_1_0[1:0],I_3_0_2[1:0],I_3_0_1[1:0],I_3_0_0[1:0],I_2_1_2[1:0],I_2_1_1[1:0],I_2_1_0[1:0],I_2_0_2[1:0],I_2_0_1[1:0],I_2_0_0[1:0],I_1_1_2[1:0],I_1_1_1[1:0],I_1_1_0[1:0],I_1_0_2[1:0],I_1_0_1[1:0],I_1_0_0[1:0],I_0_1_2[1:0],I_0_1_1[1:0],I_0_1_0[1:0],I_0_0_2[1:0],I_0_0_1[1:0],I_0_0_0[1:0]}),
    .out(reg_P_inst0_out)
);
assign O_0_0_0 = reg_P_inst0_out[1:0];
assign O_0_0_1 = reg_P_inst0_out[3:2];
assign O_0_0_2 = reg_P_inst0_out[5:4];
assign O_0_1_0 = reg_P_inst0_out[7:6];
assign O_0_1_1 = reg_P_inst0_out[9:8];
assign O_0_1_2 = reg_P_inst0_out[11:10];
assign O_1_0_0 = reg_P_inst0_out[13:12];
assign O_1_0_1 = reg_P_inst0_out[15:14];
assign O_1_0_2 = reg_P_inst0_out[17:16];
assign O_1_1_0 = reg_P_inst0_out[19:18];
assign O_1_1_1 = reg_P_inst0_out[21:20];
assign O_1_1_2 = reg_P_inst0_out[23:22];
assign O_2_0_0 = reg_P_inst0_out[25:24];
assign O_2_0_1 = reg_P_inst0_out[27:26];
assign O_2_0_2 = reg_P_inst0_out[29:28];
assign O_2_1_0 = reg_P_inst0_out[31:30];
assign O_2_1_1 = reg_P_inst0_out[33:32];
assign O_2_1_2 = reg_P_inst0_out[35:34];
assign O_3_0_0 = reg_P_inst0_out[37:36];
assign O_3_0_1 = reg_P_inst0_out[39:38];
assign O_3_0_2 = reg_P_inst0_out[41:40];
assign O_3_1_0 = reg_P_inst0_out[43:42];
assign O_3_1_1 = reg_P_inst0_out[45:44];
assign O_3_1_2 = reg_P_inst0_out[47:46];
endmodule

module Mux4xArray2_Array3_Array2_OutBit (
    input [1:0] I0_0_0,
    input [1:0] I0_0_1,
    input [1:0] I0_0_2,
    input [1:0] I0_1_0,
    input [1:0] I0_1_1,
    input [1:0] I0_1_2,
    input [1:0] I1_0_0,
    input [1:0] I1_0_1,
    input [1:0] I1_0_2,
    input [1:0] I1_1_0,
    input [1:0] I1_1_1,
    input [1:0] I1_1_2,
    input [1:0] I2_0_0,
    input [1:0] I2_0_1,
    input [1:0] I2_0_2,
    input [1:0] I2_1_0,
    input [1:0] I2_1_1,
    input [1:0] I2_1_2,
    input [1:0] I3_0_0,
    input [1:0] I3_0_1,
    input [1:0] I3_0_2,
    input [1:0] I3_1_0,
    input [1:0] I3_1_1,
    input [1:0] I3_1_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    input [1:0] S
);
reg [11:0] coreir_commonlib_mux4x12_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x12_inst0_out = {I0_1_2[1:0],I0_1_1[1:0],I0_1_0[1:0],I0_0_2[1:0],I0_0_1[1:0],I0_0_0[1:0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x12_inst0_out = {I1_1_2[1:0],I1_1_1[1:0],I1_1_0[1:0],I1_0_2[1:0],I1_0_1[1:0],I1_0_0[1:0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x12_inst0_out = {I2_1_2[1:0],I2_1_1[1:0],I2_1_0[1:0],I2_0_2[1:0],I2_0_1[1:0],I2_0_0[1:0]};
end else begin
    coreir_commonlib_mux4x12_inst0_out = {I3_1_2[1:0],I3_1_1[1:0],I3_1_0[1:0],I3_0_2[1:0],I3_0_1[1:0],I3_0_0[1:0]};
end
end

assign O_0_0 = coreir_commonlib_mux4x12_inst0_out[1:0];
assign O_0_1 = coreir_commonlib_mux4x12_inst0_out[3:2];
assign O_0_2 = coreir_commonlib_mux4x12_inst0_out[5:4];
assign O_1_0 = coreir_commonlib_mux4x12_inst0_out[7:6];
assign O_1_1 = coreir_commonlib_mux4x12_inst0_out[9:8];
assign O_1_2 = coreir_commonlib_mux4x12_inst0_out[11:10];
endmodule

module Main (
    input CLK,
    input [1:0] raddr0,
    input [1:0] raddr1,
    output [1:0] rdata0_0,
    output [1:0] rdata0_1,
    output [1:0] rdata0_2,
    output [1:0] rdata1_0,
    output [1:0] rdata1_1,
    output [1:0] rdata1_2
);
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_0;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_1;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_2;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_0;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_1;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_2;
wire [1:0] Register_inst0_O_0_0_0;
wire [1:0] Register_inst0_O_0_0_1;
wire [1:0] Register_inst0_O_0_0_2;
wire [1:0] Register_inst0_O_0_1_0;
wire [1:0] Register_inst0_O_0_1_1;
wire [1:0] Register_inst0_O_0_1_2;
wire [1:0] Register_inst0_O_1_0_0;
wire [1:0] Register_inst0_O_1_0_1;
wire [1:0] Register_inst0_O_1_0_2;
wire [1:0] Register_inst0_O_1_1_0;
wire [1:0] Register_inst0_O_1_1_1;
wire [1:0] Register_inst0_O_1_1_2;
wire [1:0] Register_inst0_O_2_0_0;
wire [1:0] Register_inst0_O_2_0_1;
wire [1:0] Register_inst0_O_2_0_2;
wire [1:0] Register_inst0_O_2_1_0;
wire [1:0] Register_inst0_O_2_1_1;
wire [1:0] Register_inst0_O_2_1_2;
wire [1:0] Register_inst0_O_3_0_0;
wire [1:0] Register_inst0_O_3_0_1;
wire [1:0] Register_inst0_O_3_0_2;
wire [1:0] Register_inst0_O_3_1_0;
wire [1:0] Register_inst0_O_3_1_1;
wire [1:0] Register_inst0_O_3_1_2;
Mux4xArray2_Array3_Array2_OutBit Mux4xArray2_Array3_Array2_OutBit_inst0 (
    .I0_0_0(Register_inst0_O_0_0_0),
    .I0_0_1(Register_inst0_O_0_0_1),
    .I0_0_2(Register_inst0_O_0_0_2),
    .I0_1_0(Register_inst0_O_0_1_0),
    .I0_1_1(Register_inst0_O_0_1_1),
    .I0_1_2(Register_inst0_O_0_1_2),
    .I1_0_0(Register_inst0_O_1_0_0),
    .I1_0_1(Register_inst0_O_1_0_1),
    .I1_0_2(Register_inst0_O_1_0_2),
    .I1_1_0(Register_inst0_O_1_1_0),
    .I1_1_1(Register_inst0_O_1_1_1),
    .I1_1_2(Register_inst0_O_1_1_2),
    .I2_0_0(Register_inst0_O_2_0_0),
    .I2_0_1(Register_inst0_O_2_0_1),
    .I2_0_2(Register_inst0_O_2_0_2),
    .I2_1_0(Register_inst0_O_2_1_0),
    .I2_1_1(Register_inst0_O_2_1_1),
    .I2_1_2(Register_inst0_O_2_1_2),
    .I3_0_0(Register_inst0_O_3_0_0),
    .I3_0_1(Register_inst0_O_3_0_1),
    .I3_0_2(Register_inst0_O_3_0_2),
    .I3_1_0(Register_inst0_O_3_1_0),
    .I3_1_1(Register_inst0_O_3_1_1),
    .I3_1_2(Register_inst0_O_3_1_2),
    .O_0_0(rdata0_0),
    .O_0_1(rdata0_1),
    .O_0_2(rdata0_2),
    .O_1_0(Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_0),
    .O_1_1(Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_1),
    .O_1_2(Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_2),
    .S(raddr0)
);
Mux4xArray2_Array3_Array2_OutBit Mux4xArray2_Array3_Array2_OutBit_inst1 (
    .I0_0_0(Register_inst0_O_0_0_0),
    .I0_0_1(Register_inst0_O_0_0_1),
    .I0_0_2(Register_inst0_O_0_0_2),
    .I0_1_0(Register_inst0_O_0_1_0),
    .I0_1_1(Register_inst0_O_0_1_1),
    .I0_1_2(Register_inst0_O_0_1_2),
    .I1_0_0(Register_inst0_O_1_0_0),
    .I1_0_1(Register_inst0_O_1_0_1),
    .I1_0_2(Register_inst0_O_1_0_2),
    .I1_1_0(Register_inst0_O_1_1_0),
    .I1_1_1(Register_inst0_O_1_1_1),
    .I1_1_2(Register_inst0_O_1_1_2),
    .I2_0_0(Register_inst0_O_2_0_0),
    .I2_0_1(Register_inst0_O_2_0_1),
    .I2_0_2(Register_inst0_O_2_0_2),
    .I2_1_0(Register_inst0_O_2_1_0),
    .I2_1_1(Register_inst0_O_2_1_1),
    .I2_1_2(Register_inst0_O_2_1_2),
    .I3_0_0(Register_inst0_O_3_0_0),
    .I3_0_1(Register_inst0_O_3_0_1),
    .I3_0_2(Register_inst0_O_3_0_2),
    .I3_1_0(Register_inst0_O_3_1_0),
    .I3_1_1(Register_inst0_O_3_1_1),
    .I3_1_2(Register_inst0_O_3_1_2),
    .O_0_0(Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_0),
    .O_0_1(Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_1),
    .O_0_2(Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_2),
    .O_1_0(rdata1_0),
    .O_1_1(rdata1_1),
    .O_1_2(rdata1_2),
    .S(raddr1)
);
Register Register_inst0 (
    .CLK(CLK),
    .I_0_0_0(Register_inst0_O_0_0_0),
    .I_0_0_1(Register_inst0_O_0_0_1),
    .I_0_0_2(Register_inst0_O_0_0_2),
    .I_0_1_0(Register_inst0_O_0_1_0),
    .I_0_1_1(Register_inst0_O_0_1_1),
    .I_0_1_2(Register_inst0_O_0_1_2),
    .I_1_0_0(Register_inst0_O_1_0_0),
    .I_1_0_1(Register_inst0_O_1_0_1),
    .I_1_0_2(Register_inst0_O_1_0_2),
    .I_1_1_0(Register_inst0_O_1_1_0),
    .I_1_1_1(Register_inst0_O_1_1_1),
    .I_1_1_2(Register_inst0_O_1_1_2),
    .I_2_0_0(Register_inst0_O_2_0_0),
    .I_2_0_1(Register_inst0_O_2_0_1),
    .I_2_0_2(Register_inst0_O_2_0_2),
    .I_2_1_0(Register_inst0_O_2_1_0),
    .I_2_1_1(Register_inst0_O_2_1_1),
    .I_2_1_2(Register_inst0_O_2_1_2),
    .I_3_0_0(Register_inst0_O_3_0_0),
    .I_3_0_1(Register_inst0_O_3_0_1),
    .I_3_0_2(Register_inst0_O_3_0_2),
    .I_3_1_0(Register_inst0_O_3_1_0),
    .I_3_1_1(Register_inst0_O_3_1_1),
    .I_3_1_2(Register_inst0_O_3_1_2),
    .O_0_0_0(Register_inst0_O_0_0_0),
    .O_0_0_1(Register_inst0_O_0_0_1),
    .O_0_0_2(Register_inst0_O_0_0_2),
    .O_0_1_0(Register_inst0_O_0_1_0),
    .O_0_1_1(Register_inst0_O_0_1_1),
    .O_0_1_2(Register_inst0_O_0_1_2),
    .O_1_0_0(Register_inst0_O_1_0_0),
    .O_1_0_1(Register_inst0_O_1_0_1),
    .O_1_0_2(Register_inst0_O_1_0_2),
    .O_1_1_0(Register_inst0_O_1_1_0),
    .O_1_1_1(Register_inst0_O_1_1_1),
    .O_1_1_2(Register_inst0_O_1_1_2),
    .O_2_0_0(Register_inst0_O_2_0_0),
    .O_2_0_1(Register_inst0_O_2_0_1),
    .O_2_0_2(Register_inst0_O_2_0_2),
    .O_2_1_0(Register_inst0_O_2_1_0),
    .O_2_1_1(Register_inst0_O_2_1_1),
    .O_2_1_2(Register_inst0_O_2_1_2),
    .O_3_0_0(Register_inst0_O_3_0_0),
    .O_3_0_1(Register_inst0_O_3_0_1),
    .O_3_0_2(Register_inst0_O_3_0_2),
    .O_3_1_0(Register_inst0_O_3_1_0),
    .O_3_1_1(Register_inst0_O_3_1_1),
    .O_3_1_2(Register_inst0_O_3_1_2)
);
endmodule


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
    input [2:0] I [1:0][3:0][1:0],
    output [2:0] O [1:0][3:0][1:0],
    input CLK
);
wire [47:0] reg_P48_inst0_out;
wire [47:0] reg_P48_inst0_in;
assign reg_P48_inst0_in = {I[1][3][1],I[1][3][0],I[1][2][1],I[1][2][0],I[1][1][1],I[1][1][0],I[1][0][1],I[1][0][0],I[0][3][1],I[0][3][0],I[0][2][1],I[0][2][0],I[0][1][1],I[0][1][0],I[0][0][1],I[0][0][0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(48'h000000000000),
    .width(48)
) reg_P48_inst0 (
    .clk(CLK),
    .in(reg_P48_inst0_in),
    .out(reg_P48_inst0_out)
);
assign O[1][3][1] = {reg_P48_inst0_out[47],reg_P48_inst0_out[46],reg_P48_inst0_out[45]};
assign O[1][3][0] = {reg_P48_inst0_out[44],reg_P48_inst0_out[43],reg_P48_inst0_out[42]};
assign O[1][2][1] = {reg_P48_inst0_out[41],reg_P48_inst0_out[40],reg_P48_inst0_out[39]};
assign O[1][2][0] = {reg_P48_inst0_out[38],reg_P48_inst0_out[37],reg_P48_inst0_out[36]};
assign O[1][1][1] = {reg_P48_inst0_out[35],reg_P48_inst0_out[34],reg_P48_inst0_out[33]};
assign O[1][1][0] = {reg_P48_inst0_out[32],reg_P48_inst0_out[31],reg_P48_inst0_out[30]};
assign O[1][0][1] = {reg_P48_inst0_out[29],reg_P48_inst0_out[28],reg_P48_inst0_out[27]};
assign O[1][0][0] = {reg_P48_inst0_out[26],reg_P48_inst0_out[25],reg_P48_inst0_out[24]};
assign O[0][3][1] = {reg_P48_inst0_out[23],reg_P48_inst0_out[22],reg_P48_inst0_out[21]};
assign O[0][3][0] = {reg_P48_inst0_out[20],reg_P48_inst0_out[19],reg_P48_inst0_out[18]};
assign O[0][2][1] = {reg_P48_inst0_out[17],reg_P48_inst0_out[16],reg_P48_inst0_out[15]};
assign O[0][2][0] = {reg_P48_inst0_out[14],reg_P48_inst0_out[13],reg_P48_inst0_out[12]};
assign O[0][1][1] = {reg_P48_inst0_out[11],reg_P48_inst0_out[10],reg_P48_inst0_out[9]};
assign O[0][1][0] = {reg_P48_inst0_out[8],reg_P48_inst0_out[7],reg_P48_inst0_out[6]};
assign O[0][0][1] = {reg_P48_inst0_out[5],reg_P48_inst0_out[4],reg_P48_inst0_out[3]};
assign O[0][0][0] = {reg_P48_inst0_out[2],reg_P48_inst0_out[1],reg_P48_inst0_out[0]};
endmodule

module Mux4xArray2_Array3_Bit (
    input [2:0] I0 [1:0],
    input [2:0] I1 [1:0],
    input [2:0] I2 [1:0],
    input [2:0] I3 [1:0],
    input [1:0] S,
    output [2:0] O [1:0]
);
reg [5:0] coreir_commonlib_mux4x6_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x6_inst0_out = {I0[1],I0[0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x6_inst0_out = {I1[1],I1[0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x6_inst0_out = {I2[1],I2[0]};
end else begin
    coreir_commonlib_mux4x6_inst0_out = {I3[1],I3[0]};
end
end

assign O[1] = {coreir_commonlib_mux4x6_inst0_out[5],coreir_commonlib_mux4x6_inst0_out[4],coreir_commonlib_mux4x6_inst0_out[3]};
assign O[0] = {coreir_commonlib_mux4x6_inst0_out[2],coreir_commonlib_mux4x6_inst0_out[1],coreir_commonlib_mux4x6_inst0_out[0]};
endmodule

module Main (
    output [2:0] rdata0 [1:0],
    input [1:0] raddr0,
    output [2:0] rdata1 [1:0],
    input [1:0] raddr1,
    input CLK
);
wire [2:0] Mux4xArray2_Array3_Bit_inst0_O [1:0];
wire [2:0] Mux4xArray2_Array3_Bit_inst1_O [1:0];
wire [2:0] Register_inst0_O [1:0][3:0][1:0];
wire [2:0] Mux4xArray2_Array3_Bit_inst0_I0 [1:0];
assign Mux4xArray2_Array3_Bit_inst0_I0[1] = Register_inst0_O[0][0][1];
assign Mux4xArray2_Array3_Bit_inst0_I0[0] = Register_inst0_O[0][0][0];
wire [2:0] Mux4xArray2_Array3_Bit_inst0_I1 [1:0];
assign Mux4xArray2_Array3_Bit_inst0_I1[1] = Register_inst0_O[0][1][1];
assign Mux4xArray2_Array3_Bit_inst0_I1[0] = Register_inst0_O[0][1][0];
wire [2:0] Mux4xArray2_Array3_Bit_inst0_I2 [1:0];
assign Mux4xArray2_Array3_Bit_inst0_I2[1] = Register_inst0_O[0][2][1];
assign Mux4xArray2_Array3_Bit_inst0_I2[0] = Register_inst0_O[0][2][0];
wire [2:0] Mux4xArray2_Array3_Bit_inst0_I3 [1:0];
assign Mux4xArray2_Array3_Bit_inst0_I3[1] = Register_inst0_O[0][3][1];
assign Mux4xArray2_Array3_Bit_inst0_I3[0] = Register_inst0_O[0][3][0];
Mux4xArray2_Array3_Bit Mux4xArray2_Array3_Bit_inst0 (
    .I0(Mux4xArray2_Array3_Bit_inst0_I0),
    .I1(Mux4xArray2_Array3_Bit_inst0_I1),
    .I2(Mux4xArray2_Array3_Bit_inst0_I2),
    .I3(Mux4xArray2_Array3_Bit_inst0_I3),
    .S(raddr0),
    .O(Mux4xArray2_Array3_Bit_inst0_O)
);
wire [2:0] Mux4xArray2_Array3_Bit_inst1_I0 [1:0];
assign Mux4xArray2_Array3_Bit_inst1_I0[1] = Register_inst0_O[1][0][1];
assign Mux4xArray2_Array3_Bit_inst1_I0[0] = Register_inst0_O[1][0][0];
wire [2:0] Mux4xArray2_Array3_Bit_inst1_I1 [1:0];
assign Mux4xArray2_Array3_Bit_inst1_I1[1] = Register_inst0_O[1][1][1];
assign Mux4xArray2_Array3_Bit_inst1_I1[0] = Register_inst0_O[1][1][0];
wire [2:0] Mux4xArray2_Array3_Bit_inst1_I2 [1:0];
assign Mux4xArray2_Array3_Bit_inst1_I2[1] = Register_inst0_O[1][2][1];
assign Mux4xArray2_Array3_Bit_inst1_I2[0] = Register_inst0_O[1][2][0];
wire [2:0] Mux4xArray2_Array3_Bit_inst1_I3 [1:0];
assign Mux4xArray2_Array3_Bit_inst1_I3[1] = Register_inst0_O[1][3][1];
assign Mux4xArray2_Array3_Bit_inst1_I3[0] = Register_inst0_O[1][3][0];
Mux4xArray2_Array3_Bit Mux4xArray2_Array3_Bit_inst1 (
    .I0(Mux4xArray2_Array3_Bit_inst1_I0),
    .I1(Mux4xArray2_Array3_Bit_inst1_I1),
    .I2(Mux4xArray2_Array3_Bit_inst1_I2),
    .I3(Mux4xArray2_Array3_Bit_inst1_I3),
    .S(raddr1),
    .O(Mux4xArray2_Array3_Bit_inst1_O)
);
wire [2:0] Register_inst0_I [1:0][3:0][1:0];
assign Register_inst0_I[1][3][1] = Register_inst0_O[1][3][1];
assign Register_inst0_I[1][3][0] = Register_inst0_O[1][3][0];
assign Register_inst0_I[1][2][1] = Register_inst0_O[1][2][1];
assign Register_inst0_I[1][2][0] = Register_inst0_O[1][2][0];
assign Register_inst0_I[1][1][1] = Register_inst0_O[1][1][1];
assign Register_inst0_I[1][1][0] = Register_inst0_O[1][1][0];
assign Register_inst0_I[1][0][1] = Register_inst0_O[1][0][1];
assign Register_inst0_I[1][0][0] = Register_inst0_O[1][0][0];
assign Register_inst0_I[0][3][1] = Register_inst0_O[0][3][1];
assign Register_inst0_I[0][3][0] = Register_inst0_O[0][3][0];
assign Register_inst0_I[0][2][1] = Register_inst0_O[0][2][1];
assign Register_inst0_I[0][2][0] = Register_inst0_O[0][2][0];
assign Register_inst0_I[0][1][1] = Register_inst0_O[0][1][1];
assign Register_inst0_I[0][1][0] = Register_inst0_O[0][1][0];
assign Register_inst0_I[0][0][1] = Register_inst0_O[0][0][1];
assign Register_inst0_I[0][0][0] = Register_inst0_O[0][0][0];
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign rdata0[1] = Mux4xArray2_Array3_Bit_inst0_O[1];
assign rdata0[0] = Mux4xArray2_Array3_Bit_inst0_O[0];
assign rdata1[1] = Mux4xArray2_Array3_Bit_inst1_O[1];
assign rdata1[0] = Mux4xArray2_Array3_Bit_inst1_O[0];
endmodule


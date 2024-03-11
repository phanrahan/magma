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
    input [2:0] I [3:0][1:0][3:0],
    output [2:0] O [3:0][1:0][3:0],
    input CLK
);
wire [95:0] reg_P96_inst0_out;
wire [95:0] reg_P96_inst0_in;
assign reg_P96_inst0_in = {I[3][1][3],I[3][1][2],I[3][1][1],I[3][1][0],I[3][0][3],I[3][0][2],I[3][0][1],I[3][0][0],I[2][1][3],I[2][1][2],I[2][1][1],I[2][1][0],I[2][0][3],I[2][0][2],I[2][0][1],I[2][0][0],I[1][1][3],I[1][1][2],I[1][1][1],I[1][1][0],I[1][0][3],I[1][0][2],I[1][0][1],I[1][0][0],I[0][1][3],I[0][1][2],I[0][1][1],I[0][1][0],I[0][0][3],I[0][0][2],I[0][0][1],I[0][0][0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(96'h000000000000000000000000),
    .width(96)
) reg_P96_inst0 (
    .clk(CLK),
    .in(reg_P96_inst0_in),
    .out(reg_P96_inst0_out)
);
assign O[3][1][3] = {reg_P96_inst0_out[95],reg_P96_inst0_out[94],reg_P96_inst0_out[93]};
assign O[3][1][2] = {reg_P96_inst0_out[92],reg_P96_inst0_out[91],reg_P96_inst0_out[90]};
assign O[3][1][1] = {reg_P96_inst0_out[89],reg_P96_inst0_out[88],reg_P96_inst0_out[87]};
assign O[3][1][0] = {reg_P96_inst0_out[86],reg_P96_inst0_out[85],reg_P96_inst0_out[84]};
assign O[3][0][3] = {reg_P96_inst0_out[83],reg_P96_inst0_out[82],reg_P96_inst0_out[81]};
assign O[3][0][2] = {reg_P96_inst0_out[80],reg_P96_inst0_out[79],reg_P96_inst0_out[78]};
assign O[3][0][1] = {reg_P96_inst0_out[77],reg_P96_inst0_out[76],reg_P96_inst0_out[75]};
assign O[3][0][0] = {reg_P96_inst0_out[74],reg_P96_inst0_out[73],reg_P96_inst0_out[72]};
assign O[2][1][3] = {reg_P96_inst0_out[71],reg_P96_inst0_out[70],reg_P96_inst0_out[69]};
assign O[2][1][2] = {reg_P96_inst0_out[68],reg_P96_inst0_out[67],reg_P96_inst0_out[66]};
assign O[2][1][1] = {reg_P96_inst0_out[65],reg_P96_inst0_out[64],reg_P96_inst0_out[63]};
assign O[2][1][0] = {reg_P96_inst0_out[62],reg_P96_inst0_out[61],reg_P96_inst0_out[60]};
assign O[2][0][3] = {reg_P96_inst0_out[59],reg_P96_inst0_out[58],reg_P96_inst0_out[57]};
assign O[2][0][2] = {reg_P96_inst0_out[56],reg_P96_inst0_out[55],reg_P96_inst0_out[54]};
assign O[2][0][1] = {reg_P96_inst0_out[53],reg_P96_inst0_out[52],reg_P96_inst0_out[51]};
assign O[2][0][0] = {reg_P96_inst0_out[50],reg_P96_inst0_out[49],reg_P96_inst0_out[48]};
assign O[1][1][3] = {reg_P96_inst0_out[47],reg_P96_inst0_out[46],reg_P96_inst0_out[45]};
assign O[1][1][2] = {reg_P96_inst0_out[44],reg_P96_inst0_out[43],reg_P96_inst0_out[42]};
assign O[1][1][1] = {reg_P96_inst0_out[41],reg_P96_inst0_out[40],reg_P96_inst0_out[39]};
assign O[1][1][0] = {reg_P96_inst0_out[38],reg_P96_inst0_out[37],reg_P96_inst0_out[36]};
assign O[1][0][3] = {reg_P96_inst0_out[35],reg_P96_inst0_out[34],reg_P96_inst0_out[33]};
assign O[1][0][2] = {reg_P96_inst0_out[32],reg_P96_inst0_out[31],reg_P96_inst0_out[30]};
assign O[1][0][1] = {reg_P96_inst0_out[29],reg_P96_inst0_out[28],reg_P96_inst0_out[27]};
assign O[1][0][0] = {reg_P96_inst0_out[26],reg_P96_inst0_out[25],reg_P96_inst0_out[24]};
assign O[0][1][3] = {reg_P96_inst0_out[23],reg_P96_inst0_out[22],reg_P96_inst0_out[21]};
assign O[0][1][2] = {reg_P96_inst0_out[20],reg_P96_inst0_out[19],reg_P96_inst0_out[18]};
assign O[0][1][1] = {reg_P96_inst0_out[17],reg_P96_inst0_out[16],reg_P96_inst0_out[15]};
assign O[0][1][0] = {reg_P96_inst0_out[14],reg_P96_inst0_out[13],reg_P96_inst0_out[12]};
assign O[0][0][3] = {reg_P96_inst0_out[11],reg_P96_inst0_out[10],reg_P96_inst0_out[9]};
assign O[0][0][2] = {reg_P96_inst0_out[8],reg_P96_inst0_out[7],reg_P96_inst0_out[6]};
assign O[0][0][1] = {reg_P96_inst0_out[5],reg_P96_inst0_out[4],reg_P96_inst0_out[3]};
assign O[0][0][0] = {reg_P96_inst0_out[2],reg_P96_inst0_out[1],reg_P96_inst0_out[0]};
endmodule

module Mux4xArray2_Array4_Array3_Bit (
    input [2:0] I0 [1:0][3:0],
    input [2:0] I1 [1:0][3:0],
    input [2:0] I2 [1:0][3:0],
    input [2:0] I3 [1:0][3:0],
    input [1:0] S,
    output [2:0] O [1:0][3:0]
);
reg [23:0] coreir_commonlib_mux4x24_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x24_inst0_out = {I0[1][3],I0[1][2],I0[1][1],I0[1][0],I0[0][3],I0[0][2],I0[0][1],I0[0][0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x24_inst0_out = {I1[1][3],I1[1][2],I1[1][1],I1[1][0],I1[0][3],I1[0][2],I1[0][1],I1[0][0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x24_inst0_out = {I2[1][3],I2[1][2],I2[1][1],I2[1][0],I2[0][3],I2[0][2],I2[0][1],I2[0][0]};
end else begin
    coreir_commonlib_mux4x24_inst0_out = {I3[1][3],I3[1][2],I3[1][1],I3[1][0],I3[0][3],I3[0][2],I3[0][1],I3[0][0]};
end
end

assign O[1][3] = {coreir_commonlib_mux4x24_inst0_out[23],coreir_commonlib_mux4x24_inst0_out[22],coreir_commonlib_mux4x24_inst0_out[21]};
assign O[1][2] = {coreir_commonlib_mux4x24_inst0_out[20],coreir_commonlib_mux4x24_inst0_out[19],coreir_commonlib_mux4x24_inst0_out[18]};
assign O[1][1] = {coreir_commonlib_mux4x24_inst0_out[17],coreir_commonlib_mux4x24_inst0_out[16],coreir_commonlib_mux4x24_inst0_out[15]};
assign O[1][0] = {coreir_commonlib_mux4x24_inst0_out[14],coreir_commonlib_mux4x24_inst0_out[13],coreir_commonlib_mux4x24_inst0_out[12]};
assign O[0][3] = {coreir_commonlib_mux4x24_inst0_out[11],coreir_commonlib_mux4x24_inst0_out[10],coreir_commonlib_mux4x24_inst0_out[9]};
assign O[0][2] = {coreir_commonlib_mux4x24_inst0_out[8],coreir_commonlib_mux4x24_inst0_out[7],coreir_commonlib_mux4x24_inst0_out[6]};
assign O[0][1] = {coreir_commonlib_mux4x24_inst0_out[5],coreir_commonlib_mux4x24_inst0_out[4],coreir_commonlib_mux4x24_inst0_out[3]};
assign O[0][0] = {coreir_commonlib_mux4x24_inst0_out[2],coreir_commonlib_mux4x24_inst0_out[1],coreir_commonlib_mux4x24_inst0_out[0]};
endmodule

module Main (
    output [2:0] rdata0 [3:0],
    input [1:0] raddr0,
    output [2:0] rdata1 [3:0],
    input [1:0] raddr1,
    input CLK
);
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst0_O [1:0][3:0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst1_O [1:0][3:0];
wire [2:0] Register_inst0_O [3:0][1:0][3:0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst0_I0 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[1][3] = Register_inst0_O[0][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[1][2] = Register_inst0_O[0][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[1][1] = Register_inst0_O[0][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[1][0] = Register_inst0_O[0][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[0][3] = Register_inst0_O[0][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[0][2] = Register_inst0_O[0][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[0][1] = Register_inst0_O[0][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I0[0][0] = Register_inst0_O[0][0][0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst0_I1 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[1][3] = Register_inst0_O[1][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[1][2] = Register_inst0_O[1][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[1][1] = Register_inst0_O[1][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[1][0] = Register_inst0_O[1][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[0][3] = Register_inst0_O[1][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[0][2] = Register_inst0_O[1][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[0][1] = Register_inst0_O[1][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I1[0][0] = Register_inst0_O[1][0][0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst0_I2 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[1][3] = Register_inst0_O[2][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[1][2] = Register_inst0_O[2][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[1][1] = Register_inst0_O[2][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[1][0] = Register_inst0_O[2][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[0][3] = Register_inst0_O[2][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[0][2] = Register_inst0_O[2][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[0][1] = Register_inst0_O[2][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I2[0][0] = Register_inst0_O[2][0][0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst0_I3 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[1][3] = Register_inst0_O[3][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[1][2] = Register_inst0_O[3][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[1][1] = Register_inst0_O[3][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[1][0] = Register_inst0_O[3][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[0][3] = Register_inst0_O[3][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[0][2] = Register_inst0_O[3][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[0][1] = Register_inst0_O[3][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst0_I3[0][0] = Register_inst0_O[3][0][0];
Mux4xArray2_Array4_Array3_Bit Mux4xArray2_Array4_Array3_Bit_inst0 (
    .I0(Mux4xArray2_Array4_Array3_Bit_inst0_I0),
    .I1(Mux4xArray2_Array4_Array3_Bit_inst0_I1),
    .I2(Mux4xArray2_Array4_Array3_Bit_inst0_I2),
    .I3(Mux4xArray2_Array4_Array3_Bit_inst0_I3),
    .S(raddr0),
    .O(Mux4xArray2_Array4_Array3_Bit_inst0_O)
);
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst1_I0 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[1][3] = Register_inst0_O[0][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[1][2] = Register_inst0_O[0][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[1][1] = Register_inst0_O[0][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[1][0] = Register_inst0_O[0][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[0][3] = Register_inst0_O[0][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[0][2] = Register_inst0_O[0][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[0][1] = Register_inst0_O[0][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I0[0][0] = Register_inst0_O[0][0][0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst1_I1 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[1][3] = Register_inst0_O[1][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[1][2] = Register_inst0_O[1][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[1][1] = Register_inst0_O[1][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[1][0] = Register_inst0_O[1][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[0][3] = Register_inst0_O[1][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[0][2] = Register_inst0_O[1][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[0][1] = Register_inst0_O[1][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I1[0][0] = Register_inst0_O[1][0][0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst1_I2 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[1][3] = Register_inst0_O[2][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[1][2] = Register_inst0_O[2][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[1][1] = Register_inst0_O[2][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[1][0] = Register_inst0_O[2][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[0][3] = Register_inst0_O[2][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[0][2] = Register_inst0_O[2][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[0][1] = Register_inst0_O[2][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I2[0][0] = Register_inst0_O[2][0][0];
wire [2:0] Mux4xArray2_Array4_Array3_Bit_inst1_I3 [1:0][3:0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[1][3] = Register_inst0_O[3][1][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[1][2] = Register_inst0_O[3][1][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[1][1] = Register_inst0_O[3][1][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[1][0] = Register_inst0_O[3][1][0];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[0][3] = Register_inst0_O[3][0][3];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[0][2] = Register_inst0_O[3][0][2];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[0][1] = Register_inst0_O[3][0][1];
assign Mux4xArray2_Array4_Array3_Bit_inst1_I3[0][0] = Register_inst0_O[3][0][0];
Mux4xArray2_Array4_Array3_Bit Mux4xArray2_Array4_Array3_Bit_inst1 (
    .I0(Mux4xArray2_Array4_Array3_Bit_inst1_I0),
    .I1(Mux4xArray2_Array4_Array3_Bit_inst1_I1),
    .I2(Mux4xArray2_Array4_Array3_Bit_inst1_I2),
    .I3(Mux4xArray2_Array4_Array3_Bit_inst1_I3),
    .S(raddr1),
    .O(Mux4xArray2_Array4_Array3_Bit_inst1_O)
);
wire [2:0] Register_inst0_I [3:0][1:0][3:0];
assign Register_inst0_I[3][1][3] = Register_inst0_O[3][1][3];
assign Register_inst0_I[3][1][2] = Register_inst0_O[3][1][2];
assign Register_inst0_I[3][1][1] = Register_inst0_O[3][1][1];
assign Register_inst0_I[3][1][0] = Register_inst0_O[3][1][0];
assign Register_inst0_I[3][0][3] = Register_inst0_O[3][0][3];
assign Register_inst0_I[3][0][2] = Register_inst0_O[3][0][2];
assign Register_inst0_I[3][0][1] = Register_inst0_O[3][0][1];
assign Register_inst0_I[3][0][0] = Register_inst0_O[3][0][0];
assign Register_inst0_I[2][1][3] = Register_inst0_O[2][1][3];
assign Register_inst0_I[2][1][2] = Register_inst0_O[2][1][2];
assign Register_inst0_I[2][1][1] = Register_inst0_O[2][1][1];
assign Register_inst0_I[2][1][0] = Register_inst0_O[2][1][0];
assign Register_inst0_I[2][0][3] = Register_inst0_O[2][0][3];
assign Register_inst0_I[2][0][2] = Register_inst0_O[2][0][2];
assign Register_inst0_I[2][0][1] = Register_inst0_O[2][0][1];
assign Register_inst0_I[2][0][0] = Register_inst0_O[2][0][0];
assign Register_inst0_I[1][1][3] = Register_inst0_O[1][1][3];
assign Register_inst0_I[1][1][2] = Register_inst0_O[1][1][2];
assign Register_inst0_I[1][1][1] = Register_inst0_O[1][1][1];
assign Register_inst0_I[1][1][0] = Register_inst0_O[1][1][0];
assign Register_inst0_I[1][0][3] = Register_inst0_O[1][0][3];
assign Register_inst0_I[1][0][2] = Register_inst0_O[1][0][2];
assign Register_inst0_I[1][0][1] = Register_inst0_O[1][0][1];
assign Register_inst0_I[1][0][0] = Register_inst0_O[1][0][0];
assign Register_inst0_I[0][1][3] = Register_inst0_O[0][1][3];
assign Register_inst0_I[0][1][2] = Register_inst0_O[0][1][2];
assign Register_inst0_I[0][1][1] = Register_inst0_O[0][1][1];
assign Register_inst0_I[0][1][0] = Register_inst0_O[0][1][0];
assign Register_inst0_I[0][0][3] = Register_inst0_O[0][0][3];
assign Register_inst0_I[0][0][2] = Register_inst0_O[0][0][2];
assign Register_inst0_I[0][0][1] = Register_inst0_O[0][0][1];
assign Register_inst0_I[0][0][0] = Register_inst0_O[0][0][0];
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign rdata0[3] = Mux4xArray2_Array4_Array3_Bit_inst0_O[0][3];
assign rdata0[2] = Mux4xArray2_Array4_Array3_Bit_inst0_O[0][2];
assign rdata0[1] = Mux4xArray2_Array4_Array3_Bit_inst0_O[0][1];
assign rdata0[0] = Mux4xArray2_Array4_Array3_Bit_inst0_O[0][0];
assign rdata1[3] = Mux4xArray2_Array4_Array3_Bit_inst1_O[1][3];
assign rdata1[2] = Mux4xArray2_Array4_Array3_Bit_inst1_O[1][2];
assign rdata1[1] = Mux4xArray2_Array4_Array3_Bit_inst1_O[1][1];
assign rdata1[0] = Mux4xArray2_Array4_Array3_Bit_inst1_O[1][0];
endmodule


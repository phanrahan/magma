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
    input [6:0] I [14:0],
    output [6:0] O [14:0],
    input CLK
);
wire [104:0] reg_P105_inst0_out;
wire [104:0] reg_P105_inst0_in;
assign reg_P105_inst0_in = {I[14],I[13],I[12],I[11],I[10],I[9],I[8],I[7],I[6],I[5],I[4],I[3],I[2],I[1],I[0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(105'h000000000000000000000000000),
    .width(105)
) reg_P105_inst0 (
    .clk(CLK),
    .in(reg_P105_inst0_in),
    .out(reg_P105_inst0_out)
);
assign O[14] = {reg_P105_inst0_out[104],reg_P105_inst0_out[103],reg_P105_inst0_out[102],reg_P105_inst0_out[101],reg_P105_inst0_out[100],reg_P105_inst0_out[99],reg_P105_inst0_out[98]};
assign O[13] = {reg_P105_inst0_out[97],reg_P105_inst0_out[96],reg_P105_inst0_out[95],reg_P105_inst0_out[94],reg_P105_inst0_out[93],reg_P105_inst0_out[92],reg_P105_inst0_out[91]};
assign O[12] = {reg_P105_inst0_out[90],reg_P105_inst0_out[89],reg_P105_inst0_out[88],reg_P105_inst0_out[87],reg_P105_inst0_out[86],reg_P105_inst0_out[85],reg_P105_inst0_out[84]};
assign O[11] = {reg_P105_inst0_out[83],reg_P105_inst0_out[82],reg_P105_inst0_out[81],reg_P105_inst0_out[80],reg_P105_inst0_out[79],reg_P105_inst0_out[78],reg_P105_inst0_out[77]};
assign O[10] = {reg_P105_inst0_out[76],reg_P105_inst0_out[75],reg_P105_inst0_out[74],reg_P105_inst0_out[73],reg_P105_inst0_out[72],reg_P105_inst0_out[71],reg_P105_inst0_out[70]};
assign O[9] = {reg_P105_inst0_out[69],reg_P105_inst0_out[68],reg_P105_inst0_out[67],reg_P105_inst0_out[66],reg_P105_inst0_out[65],reg_P105_inst0_out[64],reg_P105_inst0_out[63]};
assign O[8] = {reg_P105_inst0_out[62],reg_P105_inst0_out[61],reg_P105_inst0_out[60],reg_P105_inst0_out[59],reg_P105_inst0_out[58],reg_P105_inst0_out[57],reg_P105_inst0_out[56]};
assign O[7] = {reg_P105_inst0_out[55],reg_P105_inst0_out[54],reg_P105_inst0_out[53],reg_P105_inst0_out[52],reg_P105_inst0_out[51],reg_P105_inst0_out[50],reg_P105_inst0_out[49]};
assign O[6] = {reg_P105_inst0_out[48],reg_P105_inst0_out[47],reg_P105_inst0_out[46],reg_P105_inst0_out[45],reg_P105_inst0_out[44],reg_P105_inst0_out[43],reg_P105_inst0_out[42]};
assign O[5] = {reg_P105_inst0_out[41],reg_P105_inst0_out[40],reg_P105_inst0_out[39],reg_P105_inst0_out[38],reg_P105_inst0_out[37],reg_P105_inst0_out[36],reg_P105_inst0_out[35]};
assign O[4] = {reg_P105_inst0_out[34],reg_P105_inst0_out[33],reg_P105_inst0_out[32],reg_P105_inst0_out[31],reg_P105_inst0_out[30],reg_P105_inst0_out[29],reg_P105_inst0_out[28]};
assign O[3] = {reg_P105_inst0_out[27],reg_P105_inst0_out[26],reg_P105_inst0_out[25],reg_P105_inst0_out[24],reg_P105_inst0_out[23],reg_P105_inst0_out[22],reg_P105_inst0_out[21]};
assign O[2] = {reg_P105_inst0_out[20],reg_P105_inst0_out[19],reg_P105_inst0_out[18],reg_P105_inst0_out[17],reg_P105_inst0_out[16],reg_P105_inst0_out[15],reg_P105_inst0_out[14]};
assign O[1] = {reg_P105_inst0_out[13],reg_P105_inst0_out[12],reg_P105_inst0_out[11],reg_P105_inst0_out[10],reg_P105_inst0_out[9],reg_P105_inst0_out[8],reg_P105_inst0_out[7]};
assign O[0] = {reg_P105_inst0_out[6],reg_P105_inst0_out[5],reg_P105_inst0_out[4],reg_P105_inst0_out[3],reg_P105_inst0_out[2],reg_P105_inst0_out[1],reg_P105_inst0_out[0]};
endmodule

module Test2 (
    input [6:0] I [14:0],
    output [6:0] O [14:0],
    input CLK
);
wire [6:0] Register_inst0_O [14:0];
wire [6:0] Register_inst0_I [14:0];
assign Register_inst0_I[14] = I[14];
assign Register_inst0_I[13] = I[13];
assign Register_inst0_I[12] = I[12];
assign Register_inst0_I[11] = I[11];
assign Register_inst0_I[10] = I[10];
assign Register_inst0_I[9] = I[9];
assign Register_inst0_I[8] = I[8];
assign Register_inst0_I[7] = I[7];
assign Register_inst0_I[6] = I[6];
assign Register_inst0_I[5] = I[5];
assign Register_inst0_I[4] = I[4];
assign Register_inst0_I[3] = I[3];
assign Register_inst0_I[2] = I[2];
assign Register_inst0_I[1] = I[1];
assign Register_inst0_I[0] = I[0];
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign O[14] = Register_inst0_O[14];
assign O[13] = Register_inst0_O[13];
assign O[12] = Register_inst0_O[12];
assign O[11] = Register_inst0_O[11];
assign O[10] = Register_inst0_O[10];
assign O[9] = Register_inst0_O[9];
assign O[8] = Register_inst0_O[8];
assign O[7] = Register_inst0_O[7];
assign O[6] = Register_inst0_O[6];
assign O[5] = Register_inst0_O[5];
assign O[4] = Register_inst0_O[4];
assign O[3] = Register_inst0_O[3];
assign O[2] = Register_inst0_O[2];
assign O[1] = Register_inst0_O[1];
assign O[0] = Register_inst0_O[0];
endmodule


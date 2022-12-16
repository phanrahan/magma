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
wire [104:0] _reg_out;
wire [104:0] _reg_in;
assign _reg_in = {I[14],I[13],I[12],I[11],I[10],I[9],I[8],I[7],I[6],I[5],I[4],I[3],I[2],I[1],I[0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(105'h000000000000000000000000000),
    .width(105)
) _reg (
    .clk(CLK),
    .in(_reg_in),
    .out(_reg_out)
);
assign O[14] = {_reg_out[104],_reg_out[103],_reg_out[102],_reg_out[101],_reg_out[100],_reg_out[99],_reg_out[98]};
assign O[13] = {_reg_out[97],_reg_out[96],_reg_out[95],_reg_out[94],_reg_out[93],_reg_out[92],_reg_out[91]};
assign O[12] = {_reg_out[90],_reg_out[89],_reg_out[88],_reg_out[87],_reg_out[86],_reg_out[85],_reg_out[84]};
assign O[11] = {_reg_out[83],_reg_out[82],_reg_out[81],_reg_out[80],_reg_out[79],_reg_out[78],_reg_out[77]};
assign O[10] = {_reg_out[76],_reg_out[75],_reg_out[74],_reg_out[73],_reg_out[72],_reg_out[71],_reg_out[70]};
assign O[9] = {_reg_out[69],_reg_out[68],_reg_out[67],_reg_out[66],_reg_out[65],_reg_out[64],_reg_out[63]};
assign O[8] = {_reg_out[62],_reg_out[61],_reg_out[60],_reg_out[59],_reg_out[58],_reg_out[57],_reg_out[56]};
assign O[7] = {_reg_out[55],_reg_out[54],_reg_out[53],_reg_out[52],_reg_out[51],_reg_out[50],_reg_out[49]};
assign O[6] = {_reg_out[48],_reg_out[47],_reg_out[46],_reg_out[45],_reg_out[44],_reg_out[43],_reg_out[42]};
assign O[5] = {_reg_out[41],_reg_out[40],_reg_out[39],_reg_out[38],_reg_out[37],_reg_out[36],_reg_out[35]};
assign O[4] = {_reg_out[34],_reg_out[33],_reg_out[32],_reg_out[31],_reg_out[30],_reg_out[29],_reg_out[28]};
assign O[3] = {_reg_out[27],_reg_out[26],_reg_out[25],_reg_out[24],_reg_out[23],_reg_out[22],_reg_out[21]};
assign O[2] = {_reg_out[20],_reg_out[19],_reg_out[18],_reg_out[17],_reg_out[16],_reg_out[15],_reg_out[14]};
assign O[1] = {_reg_out[13],_reg_out[12],_reg_out[11],_reg_out[10],_reg_out[9],_reg_out[8],_reg_out[7]};
assign O[0] = {_reg_out[6],_reg_out[5],_reg_out[4],_reg_out[3],_reg_out[2],_reg_out[1],_reg_out[0]};
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


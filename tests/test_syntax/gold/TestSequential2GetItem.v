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

module Register_unq1 (
    input [2:0] I,
    output [2:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P3_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Register (
    input [6:0] I [7:0],
    output [6:0] O [7:0],
    input CLK
);
wire [55:0] reg_P56_inst0_out;
wire [55:0] reg_P56_inst0_in;
assign reg_P56_inst0_in = {I[7],I[6],I[5],I[4],I[3],I[2],I[1],I[0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(56'h00000000000000),
    .width(56)
) reg_P56_inst0 (
    .clk(CLK),
    .in(reg_P56_inst0_in),
    .out(reg_P56_inst0_out)
);
assign O[7] = {reg_P56_inst0_out[55],reg_P56_inst0_out[54],reg_P56_inst0_out[53],reg_P56_inst0_out[52],reg_P56_inst0_out[51],reg_P56_inst0_out[50],reg_P56_inst0_out[49]};
assign O[6] = {reg_P56_inst0_out[48],reg_P56_inst0_out[47],reg_P56_inst0_out[46],reg_P56_inst0_out[45],reg_P56_inst0_out[44],reg_P56_inst0_out[43],reg_P56_inst0_out[42]};
assign O[5] = {reg_P56_inst0_out[41],reg_P56_inst0_out[40],reg_P56_inst0_out[39],reg_P56_inst0_out[38],reg_P56_inst0_out[37],reg_P56_inst0_out[36],reg_P56_inst0_out[35]};
assign O[4] = {reg_P56_inst0_out[34],reg_P56_inst0_out[33],reg_P56_inst0_out[32],reg_P56_inst0_out[31],reg_P56_inst0_out[30],reg_P56_inst0_out[29],reg_P56_inst0_out[28]};
assign O[3] = {reg_P56_inst0_out[27],reg_P56_inst0_out[26],reg_P56_inst0_out[25],reg_P56_inst0_out[24],reg_P56_inst0_out[23],reg_P56_inst0_out[22],reg_P56_inst0_out[21]};
assign O[2] = {reg_P56_inst0_out[20],reg_P56_inst0_out[19],reg_P56_inst0_out[18],reg_P56_inst0_out[17],reg_P56_inst0_out[16],reg_P56_inst0_out[15],reg_P56_inst0_out[14]};
assign O[1] = {reg_P56_inst0_out[13],reg_P56_inst0_out[12],reg_P56_inst0_out[11],reg_P56_inst0_out[10],reg_P56_inst0_out[9],reg_P56_inst0_out[8],reg_P56_inst0_out[7]};
assign O[0] = {reg_P56_inst0_out[6],reg_P56_inst0_out[5],reg_P56_inst0_out[4],reg_P56_inst0_out[3],reg_P56_inst0_out[2],reg_P56_inst0_out[1],reg_P56_inst0_out[0]};
endmodule

module Mux8xBits7 (
    input [6:0] I0,
    input [6:0] I1,
    input [6:0] I2,
    input [6:0] I3,
    input [6:0] I4,
    input [6:0] I5,
    input [6:0] I6,
    input [6:0] I7,
    input [2:0] S,
    output [6:0] O
);
reg [6:0] coreir_commonlib_mux8x7_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux8x7_inst0_out = I0;
end else if (S == 1) begin
    coreir_commonlib_mux8x7_inst0_out = I1;
end else if (S == 2) begin
    coreir_commonlib_mux8x7_inst0_out = I2;
end else if (S == 3) begin
    coreir_commonlib_mux8x7_inst0_out = I3;
end else if (S == 4) begin
    coreir_commonlib_mux8x7_inst0_out = I4;
end else if (S == 5) begin
    coreir_commonlib_mux8x7_inst0_out = I5;
end else if (S == 6) begin
    coreir_commonlib_mux8x7_inst0_out = I6;
end else begin
    coreir_commonlib_mux8x7_inst0_out = I7;
end
end

assign O = coreir_commonlib_mux8x7_inst0_out;
endmodule

module Test2 (
    input [6:0] I [7:0],
    input [2:0] index,
    output [6:0] O [1:0],
    input CLK
);
wire [6:0] Mux8xBits7_inst0_O;
wire [6:0] Mux8xBits7_inst1_O;
wire [6:0] Register_inst0_O [7:0];
wire [2:0] Register_inst1_O;
Mux8xBits7 Mux8xBits7_inst0 (
    .I0(Register_inst0_O[0]),
    .I1(Register_inst0_O[1]),
    .I2(Register_inst0_O[2]),
    .I3(Register_inst0_O[3]),
    .I4(Register_inst0_O[4]),
    .I5(Register_inst0_O[5]),
    .I6(Register_inst0_O[6]),
    .I7(Register_inst0_O[7]),
    .S(index),
    .O(Mux8xBits7_inst0_O)
);
Mux8xBits7 Mux8xBits7_inst1 (
    .I0(Register_inst0_O[0]),
    .I1(Register_inst0_O[1]),
    .I2(Register_inst0_O[2]),
    .I3(Register_inst0_O[3]),
    .I4(Register_inst0_O[4]),
    .I5(Register_inst0_O[5]),
    .I6(Register_inst0_O[6]),
    .I7(Register_inst0_O[7]),
    .S(Register_inst1_O),
    .O(Mux8xBits7_inst1_O)
);
wire [6:0] Register_inst0_I [7:0];
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
Register_unq1 Register_inst1 (
    .I(index),
    .O(Register_inst1_O),
    .CLK(CLK)
);
assign O[1] = Mux8xBits7_inst1_O;
assign O[0] = Mux8xBits7_inst0_O;
endmodule


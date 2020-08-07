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
wire reg_P_inst0_clk;
wire [104:0] reg_P_inst0_in;
wire [104:0] reg_P_inst0_out;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = {I[14][6:0],I[13][6:0],I[12][6:0],I[11][6:0],I[10][6:0],I[9][6:0],I[8][6:0],I[7][6:0],I[6][6:0],I[5][6:0],I[4][6:0],I[3][6:0],I[2][6:0],I[1][6:0],I[0][6:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(105'h000000000000000000000000000),
    .width(105)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O[14] = reg_P_inst0_out[104:98];
assign O[13] = reg_P_inst0_out[97:91];
assign O[12] = reg_P_inst0_out[90:84];
assign O[11] = reg_P_inst0_out[83:77];
assign O[10] = reg_P_inst0_out[76:70];
assign O[9] = reg_P_inst0_out[69:63];
assign O[8] = reg_P_inst0_out[62:56];
assign O[7] = reg_P_inst0_out[55:49];
assign O[6] = reg_P_inst0_out[48:42];
assign O[5] = reg_P_inst0_out[41:35];
assign O[4] = reg_P_inst0_out[34:28];
assign O[3] = reg_P_inst0_out[27:21];
assign O[2] = reg_P_inst0_out[20:14];
assign O[1] = reg_P_inst0_out[13:7];
assign O[0] = reg_P_inst0_out[6:0];
endmodule

module Test2 (
    input [6:0] I [14:0],
    output [6:0] O [14:0],
    input CLK
);
wire [6:0] Register_inst0_I [14:0];
wire [6:0] Register_inst0_O [14:0];
wire Register_inst0_CLK;
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
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK)
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


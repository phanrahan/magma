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
wire reg_P_inst0_clk;
wire [2:0] reg_P_inst0_in;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(O)
);
endmodule

module Register (
    input [6:0] I [7:0],
    output [6:0] O [7:0],
    input CLK
);
wire reg_P_inst0_clk;
wire [55:0] reg_P_inst0_in;
wire [55:0] reg_P_inst0_out;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = {I[7][6:0],I[6][6:0],I[5][6:0],I[4][6:0],I[3][6:0],I[2][6:0],I[1][6:0],I[0][6:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(56'h00000000000000),
    .width(56)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O[7] = reg_P_inst0_out[55:49];
assign O[6] = reg_P_inst0_out[48:42];
assign O[5] = reg_P_inst0_out[41:35];
assign O[4] = reg_P_inst0_out[34:28];
assign O[3] = reg_P_inst0_out[27:21];
assign O[2] = reg_P_inst0_out[20:14];
assign O[1] = reg_P_inst0_out[13:7];
assign O[0] = reg_P_inst0_out[6:0];
endmodule

module Mux8xOutBits7 (
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
wire [6:0] Mux8xOutBits7_inst0_I0;
wire [6:0] Mux8xOutBits7_inst0_I1;
wire [6:0] Mux8xOutBits7_inst0_I2;
wire [6:0] Mux8xOutBits7_inst0_I3;
wire [6:0] Mux8xOutBits7_inst0_I4;
wire [6:0] Mux8xOutBits7_inst0_I5;
wire [6:0] Mux8xOutBits7_inst0_I6;
wire [6:0] Mux8xOutBits7_inst0_I7;
wire [2:0] Mux8xOutBits7_inst0_S;
wire [6:0] Mux8xOutBits7_inst0_O;
wire [6:0] Mux8xOutBits7_inst1_I0;
wire [6:0] Mux8xOutBits7_inst1_I1;
wire [6:0] Mux8xOutBits7_inst1_I2;
wire [6:0] Mux8xOutBits7_inst1_I3;
wire [6:0] Mux8xOutBits7_inst1_I4;
wire [6:0] Mux8xOutBits7_inst1_I5;
wire [6:0] Mux8xOutBits7_inst1_I6;
wire [6:0] Mux8xOutBits7_inst1_I7;
wire [2:0] Mux8xOutBits7_inst1_S;
wire [6:0] Mux8xOutBits7_inst1_O;
wire [6:0] Register_inst0_I [7:0];
wire [6:0] Register_inst0_O [7:0];
wire Register_inst0_CLK;
wire [2:0] Register_inst1_I;
wire [2:0] Register_inst1_O;
wire Register_inst1_CLK;
assign Mux8xOutBits7_inst0_I0 = Register_inst0_O[0];
assign Mux8xOutBits7_inst0_I1 = Register_inst0_O[1];
assign Mux8xOutBits7_inst0_I2 = Register_inst0_O[2];
assign Mux8xOutBits7_inst0_I3 = Register_inst0_O[3];
assign Mux8xOutBits7_inst0_I4 = Register_inst0_O[4];
assign Mux8xOutBits7_inst0_I5 = Register_inst0_O[5];
assign Mux8xOutBits7_inst0_I6 = Register_inst0_O[6];
assign Mux8xOutBits7_inst0_I7 = Register_inst0_O[7];
assign Mux8xOutBits7_inst0_S = index;
Mux8xOutBits7 Mux8xOutBits7_inst0 (
    .I0(Mux8xOutBits7_inst0_I0),
    .I1(Mux8xOutBits7_inst0_I1),
    .I2(Mux8xOutBits7_inst0_I2),
    .I3(Mux8xOutBits7_inst0_I3),
    .I4(Mux8xOutBits7_inst0_I4),
    .I5(Mux8xOutBits7_inst0_I5),
    .I6(Mux8xOutBits7_inst0_I6),
    .I7(Mux8xOutBits7_inst0_I7),
    .S(Mux8xOutBits7_inst0_S),
    .O(Mux8xOutBits7_inst0_O)
);
assign Mux8xOutBits7_inst1_I0 = Register_inst0_O[0];
assign Mux8xOutBits7_inst1_I1 = Register_inst0_O[1];
assign Mux8xOutBits7_inst1_I2 = Register_inst0_O[2];
assign Mux8xOutBits7_inst1_I3 = Register_inst0_O[3];
assign Mux8xOutBits7_inst1_I4 = Register_inst0_O[4];
assign Mux8xOutBits7_inst1_I5 = Register_inst0_O[5];
assign Mux8xOutBits7_inst1_I6 = Register_inst0_O[6];
assign Mux8xOutBits7_inst1_I7 = Register_inst0_O[7];
assign Mux8xOutBits7_inst1_S = Register_inst1_O;
Mux8xOutBits7 Mux8xOutBits7_inst1 (
    .I0(Mux8xOutBits7_inst1_I0),
    .I1(Mux8xOutBits7_inst1_I1),
    .I2(Mux8xOutBits7_inst1_I2),
    .I3(Mux8xOutBits7_inst1_I3),
    .I4(Mux8xOutBits7_inst1_I4),
    .I5(Mux8xOutBits7_inst1_I5),
    .I6(Mux8xOutBits7_inst1_I6),
    .I7(Mux8xOutBits7_inst1_I7),
    .S(Mux8xOutBits7_inst1_S),
    .O(Mux8xOutBits7_inst1_O)
);
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
assign Register_inst1_I = index;
assign Register_inst1_CLK = CLK;
Register_unq1 Register_inst1 (
    .I(Register_inst1_I),
    .O(Register_inst1_O),
    .CLK(Register_inst1_CLK)
);
assign O[1] = Mux8xOutBits7_inst1_O;
assign O[0] = Mux8xOutBits7_inst0_O;
endmodule


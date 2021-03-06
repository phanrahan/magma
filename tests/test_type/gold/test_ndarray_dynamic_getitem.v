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
    input [1:0] I [3:0][2:0],
    output [1:0] O [3:0][2:0],
    input CLK
);
wire [23:0] reg_P_inst0_out;
wire [23:0] reg_P_inst0_in;
assign reg_P_inst0_in = {I[3][2][1:0],I[3][1][1:0],I[3][0][1:0],I[2][2][1:0],I[2][1][1:0],I[2][0][1:0],I[1][2][1:0],I[1][1][1:0],I[1][0][1:0],I[0][2][1:0],I[0][1][1:0],I[0][0][1:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'h000000),
    .width(24)
) reg_P_inst0 (
    .clk(CLK),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O[3][2] = reg_P_inst0_out[23:22];
assign O[3][1] = reg_P_inst0_out[21:20];
assign O[3][0] = reg_P_inst0_out[19:18];
assign O[2][2] = reg_P_inst0_out[17:16];
assign O[2][1] = reg_P_inst0_out[15:14];
assign O[2][0] = reg_P_inst0_out[13:12];
assign O[1][2] = reg_P_inst0_out[11:10];
assign O[1][1] = reg_P_inst0_out[9:8];
assign O[1][0] = reg_P_inst0_out[7:6];
assign O[0][2] = reg_P_inst0_out[5:4];
assign O[0][1] = reg_P_inst0_out[3:2];
assign O[0][0] = reg_P_inst0_out[1:0];
endmodule

module Mux4xArray3_Array2_Bit (
    input [1:0] I0 [2:0],
    input [1:0] I1 [2:0],
    input [1:0] I2 [2:0],
    input [1:0] I3 [2:0],
    input [1:0] S,
    output [1:0] O [2:0]
);
reg [5:0] coreir_commonlib_mux4x6_inst0_out_unq1;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x6_inst0_out_unq1 = {I0[2][1:0],I0[1][1:0],I0[0][1:0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x6_inst0_out_unq1 = {I1[2][1:0],I1[1][1:0],I1[0][1:0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x6_inst0_out_unq1 = {I2[2][1:0],I2[1][1:0],I2[0][1:0]};
end else begin
    coreir_commonlib_mux4x6_inst0_out_unq1 = {I3[2][1:0],I3[1][1:0],I3[0][1:0]};
end
end

assign O[2] = coreir_commonlib_mux4x6_inst0_out_unq1[5:4];
assign O[1] = coreir_commonlib_mux4x6_inst0_out_unq1[3:2];
assign O[0] = coreir_commonlib_mux4x6_inst0_out_unq1[1:0];
endmodule

module Main (
    output [1:0] rdata [2:0],
    input [1:0] raddr,
    input CLK
);
wire [1:0] Mux4xArray3_Array2_Bit_inst0_O [2:0];
wire [1:0] Register_inst0_O [3:0][2:0];
wire [1:0] Mux4xArray3_Array2_Bit_inst0_I0 [2:0];
assign Mux4xArray3_Array2_Bit_inst0_I0[2] = Register_inst0_O[0][2];
assign Mux4xArray3_Array2_Bit_inst0_I0[1] = Register_inst0_O[0][1];
assign Mux4xArray3_Array2_Bit_inst0_I0[0] = Register_inst0_O[0][0];
wire [1:0] Mux4xArray3_Array2_Bit_inst0_I1 [2:0];
assign Mux4xArray3_Array2_Bit_inst0_I1[2] = Register_inst0_O[1][2];
assign Mux4xArray3_Array2_Bit_inst0_I1[1] = Register_inst0_O[1][1];
assign Mux4xArray3_Array2_Bit_inst0_I1[0] = Register_inst0_O[1][0];
wire [1:0] Mux4xArray3_Array2_Bit_inst0_I2 [2:0];
assign Mux4xArray3_Array2_Bit_inst0_I2[2] = Register_inst0_O[2][2];
assign Mux4xArray3_Array2_Bit_inst0_I2[1] = Register_inst0_O[2][1];
assign Mux4xArray3_Array2_Bit_inst0_I2[0] = Register_inst0_O[2][0];
wire [1:0] Mux4xArray3_Array2_Bit_inst0_I3 [2:0];
assign Mux4xArray3_Array2_Bit_inst0_I3[2] = Register_inst0_O[3][2];
assign Mux4xArray3_Array2_Bit_inst0_I3[1] = Register_inst0_O[3][1];
assign Mux4xArray3_Array2_Bit_inst0_I3[0] = Register_inst0_O[3][0];
Mux4xArray3_Array2_Bit Mux4xArray3_Array2_Bit_inst0 (
    .I0(Mux4xArray3_Array2_Bit_inst0_I0),
    .I1(Mux4xArray3_Array2_Bit_inst0_I1),
    .I2(Mux4xArray3_Array2_Bit_inst0_I2),
    .I3(Mux4xArray3_Array2_Bit_inst0_I3),
    .S(raddr),
    .O(Mux4xArray3_Array2_Bit_inst0_O)
);
wire [1:0] Register_inst0_I [3:0][2:0];
assign Register_inst0_I[3][2] = Register_inst0_O[3][2];
assign Register_inst0_I[3][1] = Register_inst0_O[3][1];
assign Register_inst0_I[3][0] = Register_inst0_O[3][0];
assign Register_inst0_I[2][2] = Register_inst0_O[2][2];
assign Register_inst0_I[2][1] = Register_inst0_O[2][1];
assign Register_inst0_I[2][0] = Register_inst0_O[2][0];
assign Register_inst0_I[1][2] = Register_inst0_O[1][2];
assign Register_inst0_I[1][1] = Register_inst0_O[1][1];
assign Register_inst0_I[1][0] = Register_inst0_O[1][0];
assign Register_inst0_I[0][2] = Register_inst0_O[0][2];
assign Register_inst0_I[0][1] = Register_inst0_O[0][1];
assign Register_inst0_I[0][0] = Register_inst0_O[0][0];
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign rdata[2] = Mux4xArray3_Array2_Bit_inst0_O[2];
assign rdata[1] = Mux4xArray3_Array2_Bit_inst0_O[1];
assign rdata[0] = Mux4xArray3_Array2_Bit_inst0_O[0];
endmodule


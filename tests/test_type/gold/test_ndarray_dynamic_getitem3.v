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
    input [1:0] I [3:0][1:0][2:0],
    output [1:0] O [3:0][1:0][2:0],
    input CLK
);
wire [47:0] _reg_out;
wire [47:0] _reg_in;
assign _reg_in = {I[3][1][2],I[3][1][1],I[3][1][0],I[3][0][2],I[3][0][1],I[3][0][0],I[2][1][2],I[2][1][1],I[2][1][0],I[2][0][2],I[2][0][1],I[2][0][0],I[1][1][2],I[1][1][1],I[1][1][0],I[1][0][2],I[1][0][1],I[1][0][0],I[0][1][2],I[0][1][1],I[0][1][0],I[0][0][2],I[0][0][1],I[0][0][0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(48'h000000000000),
    .width(48)
) _reg (
    .clk(CLK),
    .in(_reg_in),
    .out(_reg_out)
);
assign O[3][1][2] = {_reg_out[47],_reg_out[46]};
assign O[3][1][1] = {_reg_out[45],_reg_out[44]};
assign O[3][1][0] = {_reg_out[43],_reg_out[42]};
assign O[3][0][2] = {_reg_out[41],_reg_out[40]};
assign O[3][0][1] = {_reg_out[39],_reg_out[38]};
assign O[3][0][0] = {_reg_out[37],_reg_out[36]};
assign O[2][1][2] = {_reg_out[35],_reg_out[34]};
assign O[2][1][1] = {_reg_out[33],_reg_out[32]};
assign O[2][1][0] = {_reg_out[31],_reg_out[30]};
assign O[2][0][2] = {_reg_out[29],_reg_out[28]};
assign O[2][0][1] = {_reg_out[27],_reg_out[26]};
assign O[2][0][0] = {_reg_out[25],_reg_out[24]};
assign O[1][1][2] = {_reg_out[23],_reg_out[22]};
assign O[1][1][1] = {_reg_out[21],_reg_out[20]};
assign O[1][1][0] = {_reg_out[19],_reg_out[18]};
assign O[1][0][2] = {_reg_out[17],_reg_out[16]};
assign O[1][0][1] = {_reg_out[15],_reg_out[14]};
assign O[1][0][0] = {_reg_out[13],_reg_out[12]};
assign O[0][1][2] = {_reg_out[11],_reg_out[10]};
assign O[0][1][1] = {_reg_out[9],_reg_out[8]};
assign O[0][1][0] = {_reg_out[7],_reg_out[6]};
assign O[0][0][2] = {_reg_out[5],_reg_out[4]};
assign O[0][0][1] = {_reg_out[3],_reg_out[2]};
assign O[0][0][0] = {_reg_out[1],_reg_out[0]};
endmodule

module Mux4xArray2_Array3_Array2_Bit (
    input [1:0] I0 [1:0][2:0],
    input [1:0] I1 [1:0][2:0],
    input [1:0] I2 [1:0][2:0],
    input [1:0] I3 [1:0][2:0],
    input [1:0] S,
    output [1:0] O [1:0][2:0]
);
reg [11:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = {I0[1][2],I0[1][1],I0[1][0],I0[0][2],I0[0][1],I0[0][0]};
end else if (S == 1) begin
    mux_out = {I1[1][2],I1[1][1],I1[1][0],I1[0][2],I1[0][1],I1[0][0]};
end else if (S == 2) begin
    mux_out = {I2[1][2],I2[1][1],I2[1][0],I2[0][2],I2[0][1],I2[0][0]};
end else begin
    mux_out = {I3[1][2],I3[1][1],I3[1][0],I3[0][2],I3[0][1],I3[0][0]};
end
end

assign O[1][2] = {mux_out[11],mux_out[10]};
assign O[1][1] = {mux_out[9],mux_out[8]};
assign O[1][0] = {mux_out[7],mux_out[6]};
assign O[0][2] = {mux_out[5],mux_out[4]};
assign O[0][1] = {mux_out[3],mux_out[2]};
assign O[0][0] = {mux_out[1],mux_out[0]};
endmodule

module Main (
    output [1:0] rdata0 [2:0],
    input [1:0] raddr0,
    output [1:0] rdata1 [2:0],
    input [1:0] raddr1,
    input CLK
);
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_O [1:0][2:0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst1_O [1:0][2:0];
wire [1:0] mem_O [3:0][1:0][2:0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I0 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[1][2] = mem_O[0][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[1][1] = mem_O[0][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[1][0] = mem_O[0][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[0][2] = mem_O[0][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[0][1] = mem_O[0][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[0][0] = mem_O[0][0][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I1 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[1][2] = mem_O[1][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[1][1] = mem_O[1][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[1][0] = mem_O[1][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[0][2] = mem_O[1][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[0][1] = mem_O[1][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[0][0] = mem_O[1][0][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I2 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[1][2] = mem_O[2][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[1][1] = mem_O[2][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[1][0] = mem_O[2][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[0][2] = mem_O[2][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[0][1] = mem_O[2][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[0][0] = mem_O[2][0][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I3 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[1][2] = mem_O[3][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[1][1] = mem_O[3][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[1][0] = mem_O[3][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[0][2] = mem_O[3][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[0][1] = mem_O[3][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[0][0] = mem_O[3][0][0];
Mux4xArray2_Array3_Array2_Bit Mux4xArray2_Array3_Array2_Bit_inst0 (
    .I0(Mux4xArray2_Array3_Array2_Bit_inst0_I0),
    .I1(Mux4xArray2_Array3_Array2_Bit_inst0_I1),
    .I2(Mux4xArray2_Array3_Array2_Bit_inst0_I2),
    .I3(Mux4xArray2_Array3_Array2_Bit_inst0_I3),
    .S(raddr0),
    .O(Mux4xArray2_Array3_Array2_Bit_inst0_O)
);
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst1_I0 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I0[1][2] = mem_O[0][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I0[1][1] = mem_O[0][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I0[1][0] = mem_O[0][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I0[0][2] = mem_O[0][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I0[0][1] = mem_O[0][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I0[0][0] = mem_O[0][0][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst1_I1 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I1[1][2] = mem_O[1][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I1[1][1] = mem_O[1][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I1[1][0] = mem_O[1][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I1[0][2] = mem_O[1][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I1[0][1] = mem_O[1][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I1[0][0] = mem_O[1][0][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst1_I2 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I2[1][2] = mem_O[2][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I2[1][1] = mem_O[2][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I2[1][0] = mem_O[2][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I2[0][2] = mem_O[2][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I2[0][1] = mem_O[2][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I2[0][0] = mem_O[2][0][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst1_I3 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I3[1][2] = mem_O[3][1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I3[1][1] = mem_O[3][1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I3[1][0] = mem_O[3][1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I3[0][2] = mem_O[3][0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I3[0][1] = mem_O[3][0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst1_I3[0][0] = mem_O[3][0][0];
Mux4xArray2_Array3_Array2_Bit Mux4xArray2_Array3_Array2_Bit_inst1 (
    .I0(Mux4xArray2_Array3_Array2_Bit_inst1_I0),
    .I1(Mux4xArray2_Array3_Array2_Bit_inst1_I1),
    .I2(Mux4xArray2_Array3_Array2_Bit_inst1_I2),
    .I3(Mux4xArray2_Array3_Array2_Bit_inst1_I3),
    .S(raddr1),
    .O(Mux4xArray2_Array3_Array2_Bit_inst1_O)
);
wire [1:0] mem_I [3:0][1:0][2:0];
assign mem_I[3][1][2] = mem_O[3][1][2];
assign mem_I[3][1][1] = mem_O[3][1][1];
assign mem_I[3][1][0] = mem_O[3][1][0];
assign mem_I[3][0][2] = mem_O[3][0][2];
assign mem_I[3][0][1] = mem_O[3][0][1];
assign mem_I[3][0][0] = mem_O[3][0][0];
assign mem_I[2][1][2] = mem_O[2][1][2];
assign mem_I[2][1][1] = mem_O[2][1][1];
assign mem_I[2][1][0] = mem_O[2][1][0];
assign mem_I[2][0][2] = mem_O[2][0][2];
assign mem_I[2][0][1] = mem_O[2][0][1];
assign mem_I[2][0][0] = mem_O[2][0][0];
assign mem_I[1][1][2] = mem_O[1][1][2];
assign mem_I[1][1][1] = mem_O[1][1][1];
assign mem_I[1][1][0] = mem_O[1][1][0];
assign mem_I[1][0][2] = mem_O[1][0][2];
assign mem_I[1][0][1] = mem_O[1][0][1];
assign mem_I[1][0][0] = mem_O[1][0][0];
assign mem_I[0][1][2] = mem_O[0][1][2];
assign mem_I[0][1][1] = mem_O[0][1][1];
assign mem_I[0][1][0] = mem_O[0][1][0];
assign mem_I[0][0][2] = mem_O[0][0][2];
assign mem_I[0][0][1] = mem_O[0][0][1];
assign mem_I[0][0][0] = mem_O[0][0][0];
Register mem (
    .I(mem_I),
    .O(mem_O),
    .CLK(CLK)
);
assign rdata0[2] = Mux4xArray2_Array3_Array2_Bit_inst0_O[0][2];
assign rdata0[1] = Mux4xArray2_Array3_Array2_Bit_inst0_O[0][1];
assign rdata0[0] = Mux4xArray2_Array3_Array2_Bit_inst0_O[0][0];
assign rdata1[2] = Mux4xArray2_Array3_Array2_Bit_inst1_O[1][2];
assign rdata1[1] = Mux4xArray2_Array3_Array2_Bit_inst1_O[1][1];
assign rdata1[0] = Mux4xArray2_Array3_Array2_Bit_inst1_O[1][0];
endmodule


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
    input [1:0][2:0][3:0][1:0] I,
    output [1:0][2:0][3:0][1:0] O,
    input CLK
);
wire [47:0] reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(48'h000000000000),
    .width(48)
) reg_P_inst0 (
    .clk(CLK),
    .in({I[1][3][2][1:0],I[1][3][1][1:0],I[1][3][0][1:0],I[1][2][2][1:0],I[1][2][1][1:0],I[1][2][0][1:0],I[1][1][2][1:0],I[1][1][1][1:0],I[1][1][0][1:0],I[1][0][2][1:0],I[1][0][1][1:0],I[1][0][0][1:0],I[0][3][2][1:0],I[0][3][1][1:0],I[0][3][0][1:0],I[0][2][2][1:0],I[0][2][1][1:0],I[0][2][0][1:0],I[0][1][2][1:0],I[0][1][1][1:0],I[0][1][0][1:0],I[0][0][2][1:0],I[0][0][1][1:0],I[0][0][0][1:0]}),
    .out(reg_P_inst0_out)
);
assign O = {{{reg_P_inst0_out[47:46],reg_P_inst0_out[45:44],reg_P_inst0_out[43:42],reg_P_inst0_out[41:40]},{reg_P_inst0_out[39:38],reg_P_inst0_out[37:36],reg_P_inst0_out[35:34],reg_P_inst0_out[33:32]},{reg_P_inst0_out[31:30],reg_P_inst0_out[29:28],reg_P_inst0_out[27:26],reg_P_inst0_out[25:24]}},{{reg_P_inst0_out[23:22],reg_P_inst0_out[21:20],reg_P_inst0_out[19:18],reg_P_inst0_out[17:16]},{reg_P_inst0_out[15:14],reg_P_inst0_out[13:12],reg_P_inst0_out[11:10],reg_P_inst0_out[9:8]},{reg_P_inst0_out[7:6],reg_P_inst0_out[5:4],reg_P_inst0_out[3:2],reg_P_inst0_out[1:0]}}};
endmodule

module Mux4xArray3_Array2_OutBit (
    input [1:0][2:0] I0,
    input [1:0][2:0] I1,
    input [1:0][2:0] I2,
    input [1:0][2:0] I3,
    input [1:0] S,
    output [1:0][2:0] O
);
reg [5:0] coreir_commonlib_mux4x6_inst0_out;
reg [5:0][3:0] coreir_commonlib_mux4x6_inst0_in_data;
always @(*) begin
coreir_commonlib_mux4x6_inst0_in_data = {{I3[2][1:0],I3[1][1:0],I3[0][1:0]},{I2[2][1:0],I2[1][1:0],I2[0][1:0]},{I1[2][1:0],I1[1][1:0],I1[0][1:0]},{I0[2][1:0],I0[1][1:0],I0[0][1:0]}};
if (S == 0) begin
    coreir_commonlib_mux4x6_inst0_out = coreir_commonlib_mux4x6_inst0_in_data[0];
end else if (S == 1) begin
    coreir_commonlib_mux4x6_inst0_out = coreir_commonlib_mux4x6_inst0_in_data[1];
end else if (S == 2) begin
    coreir_commonlib_mux4x6_inst0_out = coreir_commonlib_mux4x6_inst0_in_data[2];
end else begin
    coreir_commonlib_mux4x6_inst0_out = coreir_commonlib_mux4x6_inst0_in_data[3];
end
end

assign O = {coreir_commonlib_mux4x6_inst0_out[5:4],{coreir_commonlib_mux4x6_inst0_out[3:2],coreir_commonlib_mux4x6_inst0_out[1:0]}};
endmodule

module Main (
    output [1:0][2:0] rdata0,
    input [1:0] raddr0,
    output [1:0][2:0] rdata1,
    input [1:0] raddr1,
    input CLK
);
wire [1:0][2:0] Mux4xArray3_Array2_OutBit_inst0_O;
wire [1:0][2:0] Mux4xArray3_Array2_OutBit_inst1_O;
wire [1:0][2:0][3:0][1:0] Register_inst0_O;
Mux4xArray3_Array2_OutBit Mux4xArray3_Array2_OutBit_inst0 (
    .I0({Register_inst0_O[0][0][2],{Register_inst0_O[0][0][1],Register_inst0_O[0][0][0]}}),
    .I1({Register_inst0_O[0][1][2],{Register_inst0_O[0][1][1],Register_inst0_O[0][1][0]}}),
    .I2({Register_inst0_O[0][2][2],{Register_inst0_O[0][2][1],Register_inst0_O[0][2][0]}}),
    .I3({Register_inst0_O[0][3][2],{Register_inst0_O[0][3][1],Register_inst0_O[0][3][0]}}),
    .S(raddr0),
    .O(Mux4xArray3_Array2_OutBit_inst0_O)
);
Mux4xArray3_Array2_OutBit Mux4xArray3_Array2_OutBit_inst1 (
    .I0({Register_inst0_O[1][0][2],{Register_inst0_O[1][0][1],Register_inst0_O[1][0][0]}}),
    .I1({Register_inst0_O[1][1][2],{Register_inst0_O[1][1][1],Register_inst0_O[1][1][0]}}),
    .I2({Register_inst0_O[1][2][2],{Register_inst0_O[1][2][1],Register_inst0_O[1][2][0]}}),
    .I3({Register_inst0_O[1][3][2],{Register_inst0_O[1][3][1],Register_inst0_O[1][3][0]}}),
    .S(raddr1),
    .O(Mux4xArray3_Array2_OutBit_inst1_O)
);
Register Register_inst0 (
    .I({{{Register_inst0_O[1][3][2],Register_inst0_O[1][3][1],Register_inst0_O[1][3][0],Register_inst0_O[1][2][2]},{Register_inst0_O[1][2][1],Register_inst0_O[1][2][0],Register_inst0_O[1][1][2],Register_inst0_O[1][1][1]},{Register_inst0_O[1][1][0],Register_inst0_O[1][0][2],Register_inst0_O[1][0][1],Register_inst0_O[1][0][0]}},{{Register_inst0_O[0][3][2],Register_inst0_O[0][3][1],Register_inst0_O[0][3][0],Register_inst0_O[0][2][2]},{Register_inst0_O[0][2][1],Register_inst0_O[0][2][0],Register_inst0_O[0][1][2],Register_inst0_O[0][1][1]},{Register_inst0_O[0][1][0],Register_inst0_O[0][0][2],Register_inst0_O[0][0][1],Register_inst0_O[0][0][0]}}}),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign rdata0 = {Mux4xArray3_Array2_OutBit_inst0_O[2],{Mux4xArray3_Array2_OutBit_inst0_O[1],Mux4xArray3_Array2_OutBit_inst0_O[0]}};
assign rdata1 = {Mux4xArray3_Array2_OutBit_inst1_O[2],{Mux4xArray3_Array2_OutBit_inst1_O[1],Mux4xArray3_Array2_OutBit_inst1_O[0]}};
endmodule


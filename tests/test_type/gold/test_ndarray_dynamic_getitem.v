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
    input [1:0][2:0][3:0] I,
    output [1:0][2:0][3:0] O,
    input CLK
);
wire [23:0] reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'h000000),
    .width(24)
) reg_P_inst0 (
    .clk(CLK),
    .in({I[3][2][1:0],I[3][1][1:0],I[3][0][1:0],I[2][2][1:0],I[2][1][1:0],I[2][0][1:0],I[1][2][1:0],I[1][1][1:0],I[1][0][1:0],I[0][2][1:0],I[0][1][1:0],I[0][0][1:0]}),
    .out(reg_P_inst0_out)
);
assign O = {{{reg_P_inst0_out[23:22],reg_P_inst0_out[21:20]},{reg_P_inst0_out[19:18],reg_P_inst0_out[17:16]},{reg_P_inst0_out[15:14],reg_P_inst0_out[13:12]}},{{reg_P_inst0_out[11:10],reg_P_inst0_out[9:8]},{reg_P_inst0_out[7:6],reg_P_inst0_out[5:4]},{reg_P_inst0_out[3:2],reg_P_inst0_out[1:0]}}};
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
    output [1:0][2:0] rdata,
    input [1:0] raddr,
    input CLK
);
wire [1:0][2:0] Mux4xArray3_Array2_OutBit_inst0_O;
wire [1:0][2:0][3:0] Register_inst0_O;
Mux4xArray3_Array2_OutBit Mux4xArray3_Array2_OutBit_inst0 (
    .I0({Register_inst0_O[0][2],{Register_inst0_O[0][1],Register_inst0_O[0][0]}}),
    .I1({Register_inst0_O[1][2],{Register_inst0_O[1][1],Register_inst0_O[1][0]}}),
    .I2({Register_inst0_O[2][2],{Register_inst0_O[2][1],Register_inst0_O[2][0]}}),
    .I3({Register_inst0_O[3][2],{Register_inst0_O[3][1],Register_inst0_O[3][0]}}),
    .S(raddr),
    .O(Mux4xArray3_Array2_OutBit_inst0_O)
);
Register Register_inst0 (
    .I({{{Register_inst0_O[3][2],Register_inst0_O[3][1]},{Register_inst0_O[3][0],Register_inst0_O[2][2]},{Register_inst0_O[2][1],Register_inst0_O[2][0]}},{{Register_inst0_O[1][2],Register_inst0_O[1][1]},{Register_inst0_O[1][0],Register_inst0_O[0][2]},{Register_inst0_O[0][1],Register_inst0_O[0][0]}}}),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign rdata = {Mux4xArray3_Array2_OutBit_inst0_O[2],{Mux4xArray3_Array2_OutBit_inst0_O[1],Mux4xArray3_Array2_OutBit_inst0_O[0]}};
endmodule


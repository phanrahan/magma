module mantle_wire__typeBitIn6 (
    output [5:0] in,
    input [5:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn2 (
    output [1:0] in,
    input [1:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit6 (
    input [5:0] in,
    output [5:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit2 (
    input [1:0] in,
    output [1:0] out
);
assign out = in;
endmodule

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
    input CLK,
    input [1:0] I_0_0,
    input [1:0] I_0_1,
    input [1:0] I_0_2,
    input [1:0] I_1_0,
    input [1:0] I_1_1,
    input [1:0] I_1_2,
    input [1:0] I_2_0,
    input [1:0] I_2_1,
    input [1:0] I_2_2,
    input [1:0] I_3_0,
    input [1:0] I_3_1,
    input [1:0] I_3_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    output [1:0] O_2_0,
    output [1:0] O_2_1,
    output [1:0] O_2_2,
    output [1:0] O_3_0,
    output [1:0] O_3_1,
    output [1:0] O_3_2
);
wire [23:0] reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'h000000),
    .width(24)
) reg_P_inst0 (
    .clk(CLK),
    .in({I_3_2[1:0],I_3_1[1:0],I_3_0[1:0],I_2_2[1:0],I_2_1[1:0],I_2_0[1:0],I_1_2[1:0],I_1_1[1:0],I_1_0[1:0],I_0_2[1:0],I_0_1[1:0],I_0_0[1:0]}),
    .out(reg_P_inst0_out)
);
assign O_0_0 = reg_P_inst0_out[1:0];
assign O_0_1 = reg_P_inst0_out[3:2];
assign O_0_2 = reg_P_inst0_out[5:4];
assign O_1_0 = reg_P_inst0_out[7:6];
assign O_1_1 = reg_P_inst0_out[9:8];
assign O_1_2 = reg_P_inst0_out[11:10];
assign O_2_0 = reg_P_inst0_out[13:12];
assign O_2_1 = reg_P_inst0_out[15:14];
assign O_2_2 = reg_P_inst0_out[17:16];
assign O_3_0 = reg_P_inst0_out[19:18];
assign O_3_1 = reg_P_inst0_out[21:20];
assign O_3_2 = reg_P_inst0_out[23:22];
endmodule

module Mux4xArray3_Array2_OutBit (
    input [1:0] I0_0,
    input [1:0] I0_1,
    input [1:0] I0_2,
    input [1:0] I1_0,
    input [1:0] I1_1,
    input [1:0] I1_2,
    input [1:0] I2_0,
    input [1:0] I2_1,
    input [1:0] I2_2,
    input [1:0] I3_0,
    input [1:0] I3_1,
    input [1:0] I3_2,
    output [1:0] O_0,
    output [1:0] O_1,
    output [1:0] O_2,
    input [1:0] S
);
reg [5:0] coreir_commonlib_mux4x6_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x6_inst0_out = {I0_2[1:0],I0_1[1:0],I0_0[1:0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x6_inst0_out = {I1_2[1:0],I1_1[1:0],I1_0[1:0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x6_inst0_out = {I2_2[1:0],I2_1[1:0],I2_0[1:0]};
end else begin
    coreir_commonlib_mux4x6_inst0_out = {I3_2[1:0],I3_1[1:0],I3_0[1:0]};
end
end

assign O_0 = coreir_commonlib_mux4x6_inst0_out[1:0];
assign O_1 = coreir_commonlib_mux4x6_inst0_out[3:2];
assign O_2 = coreir_commonlib_mux4x6_inst0_out[5:4];
endmodule

module Main (
    input CLK,
    input [1:0] raddr,
    output [1:0] rdata_0,
    output [1:0] rdata_1,
    output [1:0] rdata_2
);
wire [1:0] Register_inst0_O_0_0;
wire [1:0] Register_inst0_O_0_1;
wire [1:0] Register_inst0_O_0_2;
wire [1:0] Register_inst0_O_1_0;
wire [1:0] Register_inst0_O_1_1;
wire [1:0] Register_inst0_O_1_2;
wire [1:0] Register_inst0_O_2_0;
wire [1:0] Register_inst0_O_2_1;
wire [1:0] Register_inst0_O_2_2;
wire [1:0] Register_inst0_O_3_0;
wire [1:0] Register_inst0_O_3_1;
wire [1:0] Register_inst0_O_3_2;
Mux4xArray3_Array2_OutBit Mux4xArray3_Array2_OutBit_inst0 (
    .I0_0(Register_inst0_O_0_0),
    .I0_1(Register_inst0_O_0_1),
    .I0_2(Register_inst0_O_0_2),
    .I1_0(Register_inst0_O_1_0),
    .I1_1(Register_inst0_O_1_1),
    .I1_2(Register_inst0_O_1_2),
    .I2_0(Register_inst0_O_2_0),
    .I2_1(Register_inst0_O_2_1),
    .I2_2(Register_inst0_O_2_2),
    .I3_0(Register_inst0_O_3_0),
    .I3_1(Register_inst0_O_3_1),
    .I3_2(Register_inst0_O_3_2),
    .O_0(rdata_0),
    .O_1(rdata_1),
    .O_2(rdata_2),
    .S(raddr)
);
Register Register_inst0 (
    .CLK(CLK),
    .I_0_0(Register_inst0_O_0_0),
    .I_0_1(Register_inst0_O_0_1),
    .I_0_2(Register_inst0_O_0_2),
    .I_1_0(Register_inst0_O_1_0),
    .I_1_1(Register_inst0_O_1_1),
    .I_1_2(Register_inst0_O_1_2),
    .I_2_0(Register_inst0_O_2_0),
    .I_2_1(Register_inst0_O_2_1),
    .I_2_2(Register_inst0_O_2_2),
    .I_3_0(Register_inst0_O_3_0),
    .I_3_1(Register_inst0_O_3_1),
    .I_3_2(Register_inst0_O_3_2),
    .O_0_0(Register_inst0_O_0_0),
    .O_0_1(Register_inst0_O_0_1),
    .O_0_2(Register_inst0_O_0_2),
    .O_1_0(Register_inst0_O_1_0),
    .O_1_1(Register_inst0_O_1_1),
    .O_1_2(Register_inst0_O_1_2),
    .O_2_0(Register_inst0_O_2_0),
    .O_2_1(Register_inst0_O_2_1),
    .O_2_2(Register_inst0_O_2_2),
    .O_3_0(Register_inst0_O_3_0),
    .O_3_1(Register_inst0_O_3_1),
    .O_3_2(Register_inst0_O_3_2)
);
endmodule


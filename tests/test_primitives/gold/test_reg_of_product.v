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

module Mux2xTuplex_Bits8_y_Bits4 (
    input [7:0] I0_x,
    input [3:0] I0_y,
    input [7:0] I1_x,
    input [3:0] I1_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input S
);
reg [11:0] coreir_commonlib_mux2x12_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x12_inst0_out = {I0_y,I0_x};
end else begin
    coreir_commonlib_mux2x12_inst0_out = {I1_y,I1_x};
end
end

assign O_x = {coreir_commonlib_mux2x12_inst0_out[7],coreir_commonlib_mux2x12_inst0_out[6],coreir_commonlib_mux2x12_inst0_out[5],coreir_commonlib_mux2x12_inst0_out[4],coreir_commonlib_mux2x12_inst0_out[3],coreir_commonlib_mux2x12_inst0_out[2],coreir_commonlib_mux2x12_inst0_out[1],coreir_commonlib_mux2x12_inst0_out[0]};
assign O_y = {coreir_commonlib_mux2x12_inst0_out[11],coreir_commonlib_mux2x12_inst0_out[10],coreir_commonlib_mux2x12_inst0_out[9],coreir_commonlib_mux2x12_inst0_out[8]};
endmodule

module Register (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_x;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_y;
wire [11:0] reg_P12_inst0_out;
Mux2xTuplex_Bits8_y_Bits4 Mux2xTuplex_Bits8_y_Bits4_inst0 (
    .I0_x(I_x),
    .I0_y(I_y),
    .I1_x(8'hde),
    .I1_y(4'ha),
    .O_x(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x),
    .O_y(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y),
    .S(RESET)
);
wire [11:0] reg_P12_inst0_in;
assign reg_P12_inst0_in = {Mux2xTuplex_Bits8_y_Bits4_inst0_O_y,Mux2xTuplex_Bits8_y_Bits4_inst0_O_x};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(12'hade),
    .width(12)
) reg_P12_inst0 (
    .clk(CLK),
    .in(reg_P12_inst0_in),
    .out(reg_P12_inst0_out)
);
assign O_x = {reg_P12_inst0_out[7],reg_P12_inst0_out[6],reg_P12_inst0_out[5],reg_P12_inst0_out[4],reg_P12_inst0_out[3],reg_P12_inst0_out[2],reg_P12_inst0_out[1],reg_P12_inst0_out[0]};
assign O_y = {reg_P12_inst0_out[11],reg_P12_inst0_out[10],reg_P12_inst0_out[9],reg_P12_inst0_out[8]};
endmodule

module test_reg_of_product (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
Register Register_inst0 (
    .CLK(CLK),
    .I_x(I_x),
    .I_y(I_y),
    .O_x(O_x),
    .O_y(O_y),
    .RESET(RESET)
);
endmodule


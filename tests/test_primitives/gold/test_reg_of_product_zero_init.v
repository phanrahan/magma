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
reg [11:0] coreir_commonlib_mux2x12_inst0_out_unq1;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x12_inst0_out_unq1 = {I0_y[3:0],I0_x[7:0]};
end else begin
    coreir_commonlib_mux2x12_inst0_out_unq1 = {I1_y[3:0],I1_x[7:0]};
end
end

assign O_x = coreir_commonlib_mux2x12_inst0_out_unq1[7:0];
assign O_y = coreir_commonlib_mux2x12_inst0_out_unq1[11:8];
endmodule

module Register (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_unq1;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_unq1;
wire [11:0] reg_P12_inst0_out;
Mux2xTuplex_Bits8_y_Bits4 Mux2xTuplex_Bits8_y_Bits4_inst0 (
    .I0_x(I_x),
    .I0_y(I_y),
    .I1_x(8'h00),
    .I1_y(4'h0),
    .O_x(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_unq1),
    .O_y(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_unq1),
    .S(RESET)
);
wire [11:0] reg_P12_inst0_in;
assign reg_P12_inst0_in = {Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_unq1[3:0],Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_unq1[7:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(12'h000),
    .width(12)
) reg_P12_inst0 (
    .clk(CLK),
    .in(reg_P12_inst0_in),
    .out(reg_P12_inst0_out)
);
assign O_x = reg_P12_inst0_out[7:0];
assign O_y = reg_P12_inst0_out[11:8];
endmodule

module test_reg_of_product_zero_init (
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


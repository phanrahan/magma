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
reg [11:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = {I0_y,I0_x};
end else begin
    mux_out = {I1_y,I1_x};
end
end

assign O_x = {mux_out[7],mux_out[6],mux_out[5],mux_out[4],mux_out[3],mux_out[2],mux_out[1],mux_out[0]};
assign O_y = {mux_out[11],mux_out[10],mux_out[9],mux_out[8]};
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
wire [11:0] _reg_out;
Mux2xTuplex_Bits8_y_Bits4 Mux2xTuplex_Bits8_y_Bits4_inst0 (
    .I0_x(I_x),
    .I0_y(I_y),
    .I1_x(8'h00),
    .I1_y(4'h0),
    .O_x(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x),
    .O_y(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y),
    .S(RESET)
);
wire [11:0] _reg_in;
assign _reg_in = {Mux2xTuplex_Bits8_y_Bits4_inst0_O_y,Mux2xTuplex_Bits8_y_Bits4_inst0_O_x};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(12'h000),
    .width(12)
) _reg (
    .clk(CLK),
    .in(_reg_in),
    .out(_reg_out)
);
assign O_x = {_reg_out[7],_reg_out[6],_reg_out[5],_reg_out[4],_reg_out[3],_reg_out[2],_reg_out[1],_reg_out[0]};
assign O_y = {_reg_out[11],_reg_out[10],_reg_out[9],_reg_out[8]};
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


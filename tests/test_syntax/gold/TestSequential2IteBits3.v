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
    input I,
    output O,
    input CLK
);
wire [0:0] reg_P1_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P1_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P1_inst0_out)
);
assign O = reg_P1_inst0_out[0];
endmodule

module Mux2x_SequentialRegisterWrapperBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Mux2xTuplea_Bits8 (
    input [7:0] I0_a,
    input [7:0] I1_a,
    output [7:0] O_a,
    input S
);
reg [7:0] coreir_commonlib_mux2x8_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x8_inst0_out = I0_a;
end else begin
    coreir_commonlib_mux2x8_inst0_out = I1_a;
end
end

assign O_a = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Test (
    input CLK,
    output [7:0] O_a,
    input sel
);
wire Mux2x_SequentialRegisterWrapperBit_inst0_O;
wire Register_inst0_O;
wire [7:0] Mux2xTuplea_Bits8_inst0_I0_a;
assign Mux2xTuplea_Bits8_inst0_I0_a = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,Register_inst0_O};
wire [7:0] Mux2xTuplea_Bits8_inst0_I1_a;
assign Mux2xTuplea_Bits8_inst0_I1_a = {Register_inst0_O,Register_inst0_O,Register_inst0_O,Register_inst0_O,1'b0,1'b0,1'b0,1'b0};
Mux2xTuplea_Bits8 Mux2xTuplea_Bits8_inst0 (
    .I0_a(Mux2xTuplea_Bits8_inst0_I0_a),
    .I1_a(Mux2xTuplea_Bits8_inst0_I1_a),
    .O_a(O_a),
    .S(sel)
);
Mux2x_SequentialRegisterWrapperBit Mux2x_SequentialRegisterWrapperBit_inst0 (
    .I0(Register_inst0_O),
    .I1(Register_inst0_O),
    .S(sel),
    .O(Mux2x_SequentialRegisterWrapperBit_inst0_O)
);
Register Register_inst0 (
    .I(Mux2x_SequentialRegisterWrapperBit_inst0_O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
endmodule


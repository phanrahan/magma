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

module Mux2xTuplex_OutUInt8 (
    input [7:0] I0_x,
    input [7:0] I1_x,
    output [7:0] O_x,
    input S
);
reg [7:0] coreir_commonlib_mux2x8_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x8_inst0_out = I0_x;
end else begin
    coreir_commonlib_mux2x8_inst0_out = I1_x;
end
end

assign O_x = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Test_comb (
    output [7:0] O0_x,
    output [7:0] O1_a_x,
    input c,
    input [7:0] self_a_O_x
);
wire [7:0] Mux2xTuplex_OutUInt8_inst0_I0_x;
wire [7:0] Mux2xTuplex_OutUInt8_inst0_I1_x;
wire Mux2xTuplex_OutUInt8_inst0_S;
assign Mux2xTuplex_OutUInt8_inst0_I0_x = self_a_O_x;
assign Mux2xTuplex_OutUInt8_inst0_I1_x = self_a_O_x + 8'h01;
assign Mux2xTuplex_OutUInt8_inst0_S = c;
Mux2xTuplex_OutUInt8 Mux2xTuplex_OutUInt8_inst0 (
    .I0_x(Mux2xTuplex_OutUInt8_inst0_I0_x),
    .I1_x(Mux2xTuplex_OutUInt8_inst0_I1_x),
    .O_x(O1_a_x),
    .S(Mux2xTuplex_OutUInt8_inst0_S)
);
assign O0_x = self_a_O_x;
endmodule

module Test (
    input CLK,
    output [7:0] O_a_x,
    input c
);
wire [7:0] Test_comb_inst0_O0_x;
wire Test_comb_inst0_c;
wire [7:0] Test_comb_inst0_self_a_O_x;
wire reg_P_inst0_clk;
wire [7:0] reg_P_inst0_in;
wire [7:0] reg_P_inst0_out;
assign Test_comb_inst0_c = c;
assign Test_comb_inst0_self_a_O_x = reg_P_inst0_out;
Test_comb Test_comb_inst0 (
    .O0_x(Test_comb_inst0_O0_x),
    .O1_a_x(O_a_x),
    .c(Test_comb_inst0_c),
    .self_a_O_x(Test_comb_inst0_self_a_O_x)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = Test_comb_inst0_O0_x;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
endmodule


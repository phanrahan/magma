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
    input [1:0] I_a_a__0_0,
    input I_b,
    output [1:0] O_a_a__0_0,
    output O_b
);
wire [2:0] reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst0 (
    .clk(CLK),
    .in({I_b,I_a_a__0_0[1:0]}),
    .out(reg_P_inst0_out)
);
assign O_a_a__0_0 = reg_P_inst0_out[1:0];
assign O_b = reg_P_inst0_out[2];
endmodule

module Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit (
    input [1:0] I0_a_a__0_0,
    input I0_b,
    input [1:0] I1_a_a__0_0,
    input I1_b,
    output [1:0] O_a_a__0_0,
    output O_b,
    input S
);
reg [2:0] coreir_commonlib_mux2x3_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x3_inst0_out = {I0_b,I0_a_a__0_0[1:0]};
end else begin
    coreir_commonlib_mux2x3_inst0_out = {I1_b,I1_a_a__0_0[1:0]};
end
end

assign O_a_a__0_0 = coreir_commonlib_mux2x3_inst0_out[1:0];
assign O_b = coreir_commonlib_mux2x3_inst0_out[2];
endmodule

module Test (
    input CLK,
    output [1:0] O_a_a__0_0,
    output O_b,
    input sel
);
wire [1:0] Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst0_O_a_a__0_0;
wire Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst0_O_b;
wire [1:0] Register_inst0_O_a_a__0_0;
wire Register_inst0_O_b;
Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst0 (
    .I0_a_a__0_0(Register_inst0_O_a_a__0_0),
    .I0_b(Register_inst0_O_b),
    .I1_a_a__0_0(Register_inst0_O_a_a__0_0),
    .I1_b(Register_inst0_O_b),
    .O_a_a__0_0(Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst0_O_a_a__0_0),
    .O_b(Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst0_O_b),
    .S(sel)
);
Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst1 (
    .I0_a_a__0_0(Register_inst0_O_a_a__0_0),
    .I0_b(Register_inst0_O_b),
    .I1_a_a__0_0(2'h0),
    .I1_b(1'b0),
    .O_a_a__0_0(O_a_a__0_0),
    .O_b(O_b),
    .S(sel)
);
Register Register_inst0 (
    .CLK(CLK),
    .I_a_a__0_0(Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst0_O_a_a__0_0),
    .I_b(Mux2xTuplea_Tuplea_TupleArray1_OutBits2_b_OutBit_inst0_O_b),
    .O_a_a__0_0(Register_inst0_O_a_a__0_0),
    .O_b(Register_inst0_O_b)
);
endmodule


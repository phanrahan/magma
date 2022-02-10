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

module Register_unq1 (
    input [1:0] I,
    output [1:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_P2_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
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

module Mux2x_SequentialRegisterWrapperBits2 (
    input [1:0] I0,
    input [1:0] I1,
    input S,
    output [1:0] O
);
reg [1:0] coreir_commonlib_mux2x2_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x2_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x2_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x2_inst0_out;
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

module Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit (
    input [1:0] I0_a__0,
    input [1:0] I0_b,
    input [1:0] I1_a__0,
    input [1:0] I1_b,
    output [1:0] O_a__0,
    output [1:0] O_b,
    input S
);
reg [3:0] coreir_commonlib_mux2x4_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x4_inst0_out = {I0_b,I0_a__0[1],I0_a__0[0]};
end else begin
    coreir_commonlib_mux2x4_inst0_out = {I1_b,I1_a__0[1],I1_a__0[0]};
end
end

assign O_a__0 = {coreir_commonlib_mux2x4_inst0_out[1],coreir_commonlib_mux2x4_inst0_out[0]};
assign O_b = {coreir_commonlib_mux2x4_inst0_out[3],coreir_commonlib_mux2x4_inst0_out[2]};
endmodule

module Test (
    input CLK,
    output [1:0] O_a__0,
    output [1:0] O_b,
    input sel
);
wire Mux2x_SequentialRegisterWrapperBit_inst0_O;
wire [1:0] Mux2x_SequentialRegisterWrapperBits2_inst0_O;
wire Register_inst0_O;
wire [1:0] Register_inst1_O;
wire [1:0] Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit_inst0_I0_a__0;
assign Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit_inst0_I0_a__0 = {Register_inst0_O,Register_inst0_O};
wire [1:0] Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit_inst0_I1_b;
assign Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit_inst0_I1_b = {Register_inst0_O,Register_inst0_O};
Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit_inst0 (
    .I0_a__0(Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit_inst0_I0_a__0),
    .I0_b(Register_inst1_O),
    .I1_a__0(Register_inst1_O),
    .I1_b(Mux2xTuplea_TupleArray2__SequentialRegisterWrapperBit_b_Array2_Bit_inst0_I1_b),
    .O_a__0(O_a__0),
    .O_b(O_b),
    .S(sel)
);
Mux2x_SequentialRegisterWrapperBit Mux2x_SequentialRegisterWrapperBit_inst0 (
    .I0(Register_inst0_O),
    .I1(Register_inst0_O),
    .S(sel),
    .O(Mux2x_SequentialRegisterWrapperBit_inst0_O)
);
Mux2x_SequentialRegisterWrapperBits2 Mux2x_SequentialRegisterWrapperBits2_inst0 (
    .I0(Register_inst1_O),
    .I1(Register_inst1_O),
    .S(sel),
    .O(Mux2x_SequentialRegisterWrapperBits2_inst0_O)
);
Register Register_inst0 (
    .I(Mux2x_SequentialRegisterWrapperBit_inst0_O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
Register_unq1 Register_inst1 (
    .I(Mux2x_SequentialRegisterWrapperBits2_inst0_O),
    .O(Register_inst1_O),
    .CLK(CLK)
);
endmodule


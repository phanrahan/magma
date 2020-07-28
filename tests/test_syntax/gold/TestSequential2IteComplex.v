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
wire reg_P_inst0_clk;
wire [1:0] reg_P_inst0_in;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(O)
);
endmodule

module Register (
    input I,
    output O,
    input CLK
);
wire reg_P_inst0_clk;
wire [0:0] reg_P_inst0_in;
wire [0:0] reg_P_inst0_out;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in[0] = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O = reg_P_inst0_out[0];
endmodule

module Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit (
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
    coreir_commonlib_mux2x4_inst0_out = {I0_b[1],I0_b[0],I0_a__0[1:0]};
end else begin
    coreir_commonlib_mux2x4_inst0_out = {I1_b[1],I1_b[0],I1_a__0[1:0]};
end
end

assign O_a__0 = coreir_commonlib_mux2x4_inst0_out[1:0];
assign O_b = coreir_commonlib_mux2x4_inst0_out[3:2];
endmodule

module Mux2xOutBits2 (
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

module Mux2xOutBit (
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

module Test (
    input CLK,
    output [1:0] O_a__0,
    output [1:0] O_b,
    input sel
);
wire Mux2xOutBit_inst0_I0;
wire Mux2xOutBit_inst0_I1;
wire Mux2xOutBit_inst0_S;
wire Mux2xOutBit_inst0_O;
wire [1:0] Mux2xOutBits2_inst0_I0;
wire [1:0] Mux2xOutBits2_inst0_I1;
wire Mux2xOutBits2_inst0_S;
wire [1:0] Mux2xOutBits2_inst0_O;
wire [1:0] Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I0_a__0;
wire [1:0] Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I0_b;
wire [1:0] Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I1_a__0;
wire [1:0] Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I1_b;
wire Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_S;
wire Register_inst0_I;
wire Register_inst0_O;
wire Register_inst0_CLK;
wire [1:0] Register_inst1_I;
wire [1:0] Register_inst1_O;
wire Register_inst1_CLK;
assign Mux2xOutBit_inst0_I0 = Register_inst0_O;
assign Mux2xOutBit_inst0_I1 = Register_inst0_O;
assign Mux2xOutBit_inst0_S = sel;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(Mux2xOutBit_inst0_I0),
    .I1(Mux2xOutBit_inst0_I1),
    .S(Mux2xOutBit_inst0_S),
    .O(Mux2xOutBit_inst0_O)
);
assign Mux2xOutBits2_inst0_I0 = Register_inst1_O;
assign Mux2xOutBits2_inst0_I1 = Register_inst1_O;
assign Mux2xOutBits2_inst0_S = sel;
Mux2xOutBits2 Mux2xOutBits2_inst0 (
    .I0(Mux2xOutBits2_inst0_I0),
    .I1(Mux2xOutBits2_inst0_I1),
    .S(Mux2xOutBits2_inst0_S),
    .O(Mux2xOutBits2_inst0_O)
);
assign Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I0_a__0 = {Register_inst0_O,Register_inst0_O};
assign Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I0_b = Register_inst1_O;
assign Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I1_a__0 = Register_inst1_O;
assign Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I1_b = {Register_inst0_O,Register_inst0_O};
assign Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_S = sel;
Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0 (
    .I0_a__0(Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I0_a__0),
    .I0_b(Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I0_b),
    .I1_a__0(Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I1_a__0),
    .I1_b(Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_I1_b),
    .O_a__0(O_a__0),
    .O_b(O_b),
    .S(Mux2xTuplea_Tuple_SequentialRegisterWrapperOutBits2_b_Array2__SequentialRegisterWrapperOutBit_inst0_S)
);
assign Register_inst0_I = Mux2xOutBit_inst0_O;
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK)
);
assign Register_inst1_I = Mux2xOutBits2_inst0_O;
assign Register_inst1_CLK = CLK;
Register_unq1 Register_inst1 (
    .I(Register_inst1_I),
    .O(Register_inst1_O),
    .CLK(Register_inst1_CLK)
);
endmodule


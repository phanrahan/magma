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
    input [7:0] I,
    output [7:0] O,
    input CLK
);
wire reg_P_inst0_clk;
wire [7:0] reg_P_inst0_in;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(O)
);
endmodule

module Mux2xTuplea__SequentialRegisterWrapperOutBits8 (
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

module Mux2xOutBits8 (
    input [7:0] I0,
    input [7:0] I1,
    input S,
    output [7:0] O
);
reg [7:0] coreir_commonlib_mux2x8_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x8_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x8_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Test (
    input CLK,
    output [7:0] O_a,
    input sel
);
wire [7:0] Mux2xOutBits8_inst0_I0;
wire [7:0] Mux2xOutBits8_inst0_I1;
wire Mux2xOutBits8_inst0_S;
wire [7:0] Mux2xOutBits8_inst0_O;
wire [7:0] Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_I0_a;
wire [7:0] Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_I1_a;
wire Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_S;
wire [7:0] Register_inst0_I;
wire [7:0] Register_inst0_O;
wire Register_inst0_CLK;
assign Mux2xOutBits8_inst0_I0 = Register_inst0_O;
assign Mux2xOutBits8_inst0_I1 = Register_inst0_O;
assign Mux2xOutBits8_inst0_S = sel;
Mux2xOutBits8 Mux2xOutBits8_inst0 (
    .I0(Mux2xOutBits8_inst0_I0),
    .I1(Mux2xOutBits8_inst0_I1),
    .S(Mux2xOutBits8_inst0_S),
    .O(Mux2xOutBits8_inst0_O)
);
assign Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_I0_a = Register_inst0_O;
assign Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_I1_a = Register_inst0_O;
assign Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_S = sel;
Mux2xTuplea__SequentialRegisterWrapperOutBits8 Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0 (
    .I0_a(Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_I0_a),
    .I1_a(Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_I1_a),
    .O_a(O_a),
    .S(Mux2xTuplea__SequentialRegisterWrapperOutBits8_inst0_S)
);
assign Register_inst0_I = Mux2xOutBits8_inst0_O;
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK)
);
endmodule


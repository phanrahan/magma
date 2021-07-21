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
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P8_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Mux2x_SequentialRegisterWrapperBits8 (
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

module Mux2xTuplea__SequentialRegisterWrapperBits8 (
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
wire [7:0] Mux2x_SequentialRegisterWrapperBits8_inst0_O;
wire [7:0] Register_inst0_O;
Mux2xTuplea__SequentialRegisterWrapperBits8 Mux2xTuplea__SequentialRegisterWrapperBits8_inst0 (
    .I0_a(Register_inst0_O),
    .I1_a(8'h00),
    .O_a(O_a),
    .S(sel)
);
Mux2x_SequentialRegisterWrapperBits8 Mux2x_SequentialRegisterWrapperBits8_inst0 (
    .I0(Register_inst0_O),
    .I1(Register_inst0_O),
    .S(sel),
    .O(Mux2x_SequentialRegisterWrapperBits8_inst0_O)
);
Register Register_inst0 (
    .I(Mux2x_SequentialRegisterWrapperBits8_inst0_O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
endmodule


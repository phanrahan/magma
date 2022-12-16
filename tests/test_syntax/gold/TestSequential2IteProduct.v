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
wire [0:0] _reg_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) _reg (
    .clk(CLK),
    .in(I),
    .out(_reg_out)
);
assign O = _reg_out[0];
endmodule

module Mux2xTuplea__SequentialRegisterWrapperBit (
    input I0_a,
    input I1_a,
    output O_a,
    input S
);
reg [0:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = I0_a;
end else begin
    mux_out = I1_a;
end
end

assign O_a = mux_out[0];
endmodule

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = I0;
end else begin
    mux_out = I1;
end
end

assign O = mux_out[0];
endmodule

module Test (
    input CLK,
    output O_a,
    input sel
);
wire Mux2xBit_inst0_O;
wire Register_inst0_O;
Mux2xBit Mux2xBit_inst0 (
    .I0(sel),
    .I1(sel),
    .S(sel),
    .O(Mux2xBit_inst0_O)
);
Mux2xTuplea__SequentialRegisterWrapperBit Mux2xTuplea__SequentialRegisterWrapperBit_inst0 (
    .I0_a(Register_inst0_O),
    .I1_a(Register_inst0_O),
    .O_a(O_a),
    .S(sel)
);
Register Register_inst0 (
    .I(Mux2xBit_inst0_O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
endmodule


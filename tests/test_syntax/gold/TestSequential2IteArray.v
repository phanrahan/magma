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

module Mux2xBit (
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

module Mux2xArray1__SequentialRegisterWrapperBit (
    input [0:0] I0,
    input [0:0] I1,
    input S,
    output [0:0] O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out;
endmodule

module Test (
    input sel,
    output [0:0] O,
    input CLK
);
wire Mux2xBit_inst0_O;
wire Register_inst0_O;
Mux2xArray1__SequentialRegisterWrapperBit Mux2xArray1__SequentialRegisterWrapperBit_inst0 (
    .I0(Register_inst0_O),
    .I1(1'b0),
    .S(sel),
    .O(O)
);
Mux2xBit Mux2xBit_inst0 (
    .I0(sel),
    .I1(sel),
    .S(sel),
    .O(Mux2xBit_inst0_O)
);
Register Register_inst0 (
    .I(Mux2xBit_inst0_O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
endmodule


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

module Mux2xOutBits4 (
    input [3:0] I0,
    input [3:0] I1,
    input S,
    output [3:0] O
);
reg [3:0] coreir_commonlib_mux2x4_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x4_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x4_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x4_inst0_out;
endmodule

module Basic (
    input [3:0] I,
    input S,
    output [3:0] O0,
    output [3:0] O1,
    input CLK
);
wire [3:0] Mux2xOutBits4_inst0_O;
wire [3:0] Mux2xOutBits4_inst1_O;
wire [3:0] reg_P_inst0_out;
wire [3:0] reg_P_inst1_out;
Mux2xOutBits4 Mux2xOutBits4_inst0 (
    .I0(reg_P_inst0_out),
    .I1(reg_P_inst0_out),
    .S(S),
    .O(Mux2xOutBits4_inst0_O)
);
Mux2xOutBits4 Mux2xOutBits4_inst1 (
    .I0(I),
    .I1(I),
    .S(S),
    .O(Mux2xOutBits4_inst1_O)
);
Mux2xOutBits4 Mux2xOutBits4_inst2 (
    .I0(reg_P_inst0_out),
    .I1(I),
    .S(S),
    .O(O0)
);
Mux2xOutBits4 Mux2xOutBits4_inst3 (
    .I0(I),
    .I1(reg_P_inst0_out),
    .S(S),
    .O(O1)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst0 (
    .clk(CLK),
    .in(Mux2xOutBits4_inst1_O),
    .out(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst1 (
    .clk(CLK),
    .in(Mux2xOutBits4_inst0_O),
    .out(reg_P_inst1_out)
);
endmodule


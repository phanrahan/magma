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

module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module commonlib_muxn__N2__width8 (
    input [7:0] in_data_0,
    input [7:0] in_data_1,
    input [0:0] in_sel,
    output [7:0] out
);
wire [7:0] _join_out;
coreir_mux #(
    .width(8)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutBits8 (
    input [7:0] I0,
    input [7:0] I1,
    input S,
    output [7:0] O
);
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Mux2xTuplea0_OutBits8_a1_OutBits8 (
    input [7:0] I0_a0,
    input [7:0] I0_a1,
    input [7:0] I1_a0,
    input [7:0] I1_a1,
    output [7:0] O_a0,
    output [7:0] O_a1,
    input S
);
wire [7:0] Mux2xOutBits8_inst0_O;
wire [7:0] Mux2xOutBits8_inst1_O;
Mux2xOutBits8 Mux2xOutBits8_inst0 (
    .I0(I0_a0),
    .I1(I1_a0),
    .S(S),
    .O(Mux2xOutBits8_inst0_O)
);
Mux2xOutBits8 Mux2xOutBits8_inst1 (
    .I0(I0_a1),
    .I1(I1_a1),
    .S(S),
    .O(Mux2xOutBits8_inst1_O)
);
assign O_a0 = Mux2xOutBits8_inst0_O;
assign O_a1 = Mux2xOutBits8_inst1_O;
endmodule

module TestProductAccess_comb (
    output [7:0] O0_a0,
    output [7:0] O0_a1,
    output [7:0] O1_a0,
    output [7:0] O1_a1,
    input sel,
    input [7:0] self_a_O_a0,
    input [7:0] self_a_O_a1,
    input [7:0] value
);
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
wire [7:0] Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
Mux2xTuplea0_OutBits8_a1_OutBits8 Mux2xTuplea0_OutBits8_a1_OutBits8_inst0 (
    .I0_a0(self_a_O_a0),
    .I0_a1(value),
    .I1_a0(value),
    .I1_a1(self_a_O_a1),
    .O_a0(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0),
    .O_a1(Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1),
    .S(sel)
);
assign O0_a0 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
assign O0_a1 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
assign O1_a0 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a0;
assign O1_a1 = Mux2xTuplea0_OutBits8_a1_OutBits8_inst0_O_a1;
endmodule

module TestProductAccess (
    input CLK,
    output [7:0] O_a0,
    output [7:0] O_a1,
    input sel,
    input [7:0] value
);
wire [7:0] TestProductAccess_comb_inst0_O0_a0;
wire [7:0] TestProductAccess_comb_inst0_O0_a1;
wire [7:0] TestProductAccess_comb_inst0_O1_a0;
wire [7:0] TestProductAccess_comb_inst0_O1_a1;
wire [7:0] reg_P_inst0_out;
wire [7:0] reg_P_inst1_out;
TestProductAccess_comb TestProductAccess_comb_inst0 (
    .O0_a0(TestProductAccess_comb_inst0_O0_a0),
    .O0_a1(TestProductAccess_comb_inst0_O0_a1),
    .O1_a0(TestProductAccess_comb_inst0_O1_a0),
    .O1_a1(TestProductAccess_comb_inst0_O1_a1),
    .sel(sel),
    .self_a_O_a0(reg_P_inst0_out),
    .self_a_O_a1(reg_P_inst1_out),
    .value(value)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(CLK),
    .in(TestProductAccess_comb_inst0_O0_a0),
    .out(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst1 (
    .clk(CLK),
    .in(TestProductAccess_comb_inst0_O0_a1),
    .out(reg_P_inst1_out)
);
assign O_a0 = TestProductAccess_comb_inst0_O1_a0;
assign O_a1 = TestProductAccess_comb_inst0_O1_a1;
endmodule


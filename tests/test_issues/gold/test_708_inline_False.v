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

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module commonlib_muxn__N2__width8 (
    input [1:0][7:0] in_data,
    input [0:0] in_sel,
    output [7:0] out
);
wire [7:0] _join_out;
coreir_mux #(
    .width(8)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTuplex_OutUInt8 (
    input [7:0] I0_x,
    input [7:0] I1_x,
    output [7:0] O_x,
    input S
);
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data({I1_x,I0_x}),
    .in_sel(S),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O_x = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Test_comb (
    output [7:0] O0_x,
    output [7:0] O1_a_x,
    input c,
    input [7:0] self_a_O_x
);
wire [7:0] Mux2xTuplex_OutUInt8_inst0_O_x;
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_add_inst0_out;
Mux2xTuplex_OutUInt8 Mux2xTuplex_OutUInt8_inst0 (
    .I0_x(self_a_O_x),
    .I1_x(magma_Bits_8_add_inst0_out),
    .O_x(Mux2xTuplex_OutUInt8_inst0_O_x),
    .S(c)
);
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
coreir_add #(
    .width(8)
) magma_Bits_8_add_inst0 (
    .in0(self_a_O_x),
    .in1(const_1_8_out),
    .out(magma_Bits_8_add_inst0_out)
);
assign O0_x = self_a_O_x;
assign O1_a_x = Mux2xTuplex_OutUInt8_inst0_O_x;
endmodule

module Test (
    input CLK,
    output [7:0] O_a_x,
    input c
);
wire [7:0] Test_comb_inst0_O0_x;
wire [7:0] Test_comb_inst0_O1_a_x;
wire [7:0] reg_P_inst0_out;
Test_comb Test_comb_inst0 (
    .O0_x(Test_comb_inst0_O0_x),
    .O1_a_x(Test_comb_inst0_O1_a_x),
    .c(c),
    .self_a_O_x(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(CLK),
    .in(Test_comb_inst0_O0_x),
    .out(reg_P_inst0_out)
);
assign O_a_x = Test_comb_inst0_O1_a_x;
endmodule


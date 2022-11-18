module coreir_xorr #(
    parameter width = 1
) (
    input [width-1:0] in,
    output out
);
  assign out = ^in;
endmodule

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

module coreir_orr #(
    parameter width = 1
) (
    input [width-1:0] in,
    output out
);
  assign out = |in;
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

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module commonlib_muxn__N2__width1 (
    input [0:0] in_data [1:0],
    input [0:0] in_sel,
    output [0:0] out
);
wire [0:0] _join_out;
coreir_mux #(
    .width(1)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Register (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] reg_P4_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P4_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P4_inst0_out)
);
assign O = reg_P4_inst0_out;
endmodule

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
wire [0:0] coreir_commonlib_mux2x1_inst0_in_data [1:0];
assign coreir_commonlib_mux2x1_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x1_inst0_in_data[0] = I0;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data(coreir_commonlib_mux2x1_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Foo (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] Register_inst0_O;
wire [3:0] Register_inst1_O;
Register Register_inst0 (
    .I(I),
    .O(Register_inst0_O),
    .CLK(CLK)
);
Register Register_inst1 (
    .I(Register_inst0_O),
    .O(Register_inst1_O),
    .CLK(CLK)
);
assign O = Register_inst1_O;
endmodule

module Bar (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] Foo_inst0_O;
wire [3:0] Foo_inst1_O;
wire Mux2xBit_inst0_O;
wire bit_const_0_None_out;
wire coreir_orr_3_inst0_out;
wire coreir_xorr_3_inst0_out;
Foo Foo_inst0 (
    .I(Foo_inst1_O),
    .O(Foo_inst0_O),
    .CLK(CLK)
);
wire [3:0] Foo_inst1_I;
assign Foo_inst1_I = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,Mux2xBit_inst0_O};
Foo Foo_inst1 (
    .I(Foo_inst1_I),
    .O(Foo_inst1_O),
    .CLK(CLK)
);
Mux2xBit Mux2xBit_inst0 (
    .I0(coreir_xorr_3_inst0_out),
    .I1(coreir_orr_3_inst0_out),
    .S(I[0]),
    .O(Mux2xBit_inst0_O)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_orr #(
    .width(3)
) coreir_orr_3_inst0 (
    .in(I[3:1]),
    .out(coreir_orr_3_inst0_out)
);
coreir_xorr #(
    .width(3)
) coreir_xorr_3_inst0 (
    .in(I[3:1]),
    .out(coreir_xorr_3_inst0_out)
);
assign O = Foo_inst1_O;
endmodule


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
    input CLK,
    input [1:0] I_a [0:0],
    input [1:0] I_b__0_c,
    output [1:0] O_a [0:0],
    output [1:0] O_b__0_c
);
wire [1:0] _$_U6;
wire reg_P_inst0_clk;
wire [3:0] reg_P_inst0_in;
wire [3:0] reg_P_inst0_out;
assign _$_U6 = I_a[0];
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = {I_b__0_c[1:0],_$_U6[1:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O_a[0] = reg_P_inst0_out[1:0];
assign O_b__0_c = reg_P_inst0_out[3:2];
endmodule

module Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit (
    input [1:0] I0_a [0:0],
    input [1:0] I0_b__0_c,
    input [1:0] I1_a [0:0],
    input [1:0] I1_b__0_c,
    output [1:0] O_a [0:0],
    output [1:0] O_b__0_c,
    input S
);
wire [1:0] _$_U12;
wire [1:0] _$_U14;
reg [3:0] coreir_commonlib_mux2x4_inst0_out;
assign _$_U12 = I0_a[0];
assign _$_U14 = I1_a[0];
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x4_inst0_out = {I0_b__0_c[1:0],_$_U12[1:0]};
end else begin
    coreir_commonlib_mux2x4_inst0_out = {I1_b__0_c[1:0],_$_U14[1:0]};
end
end

assign O_a[0] = coreir_commonlib_mux2x4_inst0_out[1:0];
assign O_b__0_c = coreir_commonlib_mux2x4_inst0_out[3:2];
endmodule

module Test (
    input CLK,
    output [1:0] O_a [0:0],
    output [1:0] O_b__0_c,
    input sel
);
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I0_a [0:0];
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I0_b__0_c;
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I1_a [0:0];
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I1_b__0_c;
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_O_a [0:0];
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_O_b__0_c;
wire Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_S;
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I0_a [0:0];
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I0_b__0_c;
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I1_a [0:0];
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I1_b__0_c;
wire [1:0] Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_O_a [0:0];
wire Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_S;
wire Register_inst0_CLK;
wire [1:0] Register_inst0_I_a [0:0];
wire [1:0] Register_inst0_I_b__0_c;
wire [1:0] Register_inst0_O_a [0:0];
wire [1:0] Register_inst0_O_b__0_c;
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I0_a[0] = Register_inst0_O_a[0];
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I0_b__0_c = Register_inst0_O_b__0_c;
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I1_a[0] = Register_inst0_O_a[0];
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I1_b__0_c = Register_inst0_O_b__0_c;
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_S = sel;
Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0 (
    .I0_a(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I0_a),
    .I0_b__0_c(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I0_b__0_c),
    .I1_a(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I1_a),
    .I1_b__0_c(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_I1_b__0_c),
    .O_a(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_O_a),
    .O_b__0_c(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_O_b__0_c),
    .S(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_S)
);
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I0_a[0] = Register_inst0_O_a[0];
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I0_b__0_c = Register_inst0_O_b__0_c;
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I1_a[0] = Register_inst0_O_a[0];
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I1_b__0_c = Register_inst0_O_b__0_c;
assign Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_S = sel;
Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1 (
    .I0_a(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I0_a),
    .I0_b__0_c(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I0_b__0_c),
    .I1_a(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I1_a),
    .I1_b__0_c(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_I1_b__0_c),
    .O_a(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_O_a),
    .O_b__0_c(O_b__0_c),
    .S(Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_S)
);
assign Register_inst0_CLK = CLK;
assign Register_inst0_I_a[0] = Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_O_a[0];
assign Register_inst0_I_b__0_c = Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst0_O_b__0_c;
Register Register_inst0 (
    .CLK(Register_inst0_CLK),
    .I_a(Register_inst0_I_a),
    .I_b__0_c(Register_inst0_I_b__0_c),
    .O_a(Register_inst0_O_a),
    .O_b__0_c(Register_inst0_O_b__0_c)
);
assign O_a[0] = Mux2xTuplea_Array1_OutBits2_b_TupleTuplec_Array2_OutBit_inst1_O_a[0];
endmodule


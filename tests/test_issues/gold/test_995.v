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

module corebit_term (
    input in
);

endmodule

module Register_unq1 (
    input [1:0] I,
    output [1:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_P2_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Mux3xUInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input [15:0] I2,
    input [1:0] S,
    output [15:0] O
);
reg [15:0] coreir_commonlib_mux3x16_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux3x16_inst0_out = I0;
end else if (S == 1) begin
    coreir_commonlib_mux3x16_inst0_out = I1;
end else begin
    coreir_commonlib_mux3x16_inst0_out = I2;
end
end

assign O = coreir_commonlib_mux3x16_inst0_out;
endmodule

module Mux2xUInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input S,
    output [15:0] O
);
reg [15:0] coreir_commonlib_mux2x16_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x16_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x16_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x16_inst0_out;
endmodule

module Register (
    input [15:0] I,
    output [15:0] O,
    input CE,
    input CLK
);
wire [15:0] enable_mux_O;
Mux2xUInt16 enable_mux (
    .I0(O),
    .I1(I),
    .S(CE),
    .O(enable_mux_O)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(16'h0000),
    .width(16)
) reg_P16_inst0 (
    .clk(CLK),
    .in(enable_mux_O),
    .out(O)
);
endmodule

module Mux2xBits2 (
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

module Mux2xBits1 (
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

module f3 (
    output O__0,
    output O__1,
    output [1:0] O__2,
    output O__3,
    output [0:0] O__4,
    output O__5,
    input [1:0] curr,
    input is_a_lt_b,
    input is_b_zero
);
wire Mux2xBit_inst0_O;
wire Mux2xBit_inst1_O;
wire Mux2xBit_inst2_O;
wire Mux2xBit_inst3_O;
wire Mux2xBit_inst4_O;
wire Mux2xBit_inst5_O;
wire Mux2xBit_inst6_O;
wire Mux2xBit_inst7_O;
wire [0:0] Mux2xBits1_inst0_O;
wire [0:0] Mux2xBits1_inst1_O;
wire [1:0] Mux2xBits2_inst0_O;
wire [1:0] Mux2xBits2_inst1_O;
wire [1:0] Mux2xBits2_inst2_O;
wire [6:0] __0_return_0;
wire _cond_0;
wire _cond_2;
wire _cond_3;
wire [1:0] a_mux_sel_0;
wire [1:0] a_mux_sel_1;
wire [1:0] a_mux_sel_2;
wire [1:0] a_mux_sel_3;
wire [1:0] a_mux_sel_4;
wire [1:0] a_mux_sel_5;
wire a_reg_en_0;
wire a_reg_en_1;
wire a_reg_en_2;
wire a_reg_en_3;
wire [0:0] b_mux_sel_0;
wire [0:0] b_mux_sel_1;
wire [0:0] b_mux_sel_2;
wire [0:0] b_mux_sel_3;
wire b_reg_en_0;
wire b_reg_en_1;
wire b_reg_en_2;
wire b_reg_en_3;
wire do_swap_0;
wire magma_Bit_not_inst0_out;
wire magma_Bits_2_eq_inst2_out;
wire req_rdy_0;
wire req_rdy_1;
wire req_rdy_2;
wire req_rdy_3;
wire resp_val_0;
wire resp_val_1;
wire resp_val_2;
wire resp_val_3;
Mux2xBit Mux2xBit_inst0 (
    .I0(a_reg_en_2),
    .I1(a_reg_en_1),
    .S(_cond_2),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(b_reg_en_2),
    .I1(b_reg_en_1),
    .S(_cond_2),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(req_rdy_2),
    .I1(req_rdy_1),
    .S(_cond_2),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(resp_val_2),
    .I1(resp_val_1),
    .S(_cond_2),
    .O(Mux2xBit_inst3_O)
);
Mux2xBit Mux2xBit_inst4 (
    .I0(a_reg_en_3),
    .I1(a_reg_en_0),
    .S(_cond_3),
    .O(Mux2xBit_inst4_O)
);
Mux2xBit Mux2xBit_inst5 (
    .I0(b_reg_en_3),
    .I1(b_reg_en_0),
    .S(_cond_3),
    .O(Mux2xBit_inst5_O)
);
Mux2xBit Mux2xBit_inst6 (
    .I0(req_rdy_3),
    .I1(req_rdy_0),
    .S(_cond_3),
    .O(Mux2xBit_inst6_O)
);
Mux2xBit Mux2xBit_inst7 (
    .I0(resp_val_3),
    .I1(resp_val_0),
    .S(_cond_3),
    .O(Mux2xBit_inst7_O)
);
Mux2xBits1 Mux2xBits1_inst0 (
    .I0(b_mux_sel_2),
    .I1(b_mux_sel_1),
    .S(_cond_2),
    .O(Mux2xBits1_inst0_O)
);
Mux2xBits1 Mux2xBits1_inst1 (
    .I0(b_mux_sel_3),
    .I1(b_mux_sel_0),
    .S(_cond_3),
    .O(Mux2xBits1_inst1_O)
);
Mux2xBits2 Mux2xBits2_inst0 (
    .I0(a_mux_sel_2),
    .I1(a_mux_sel_1),
    .S(_cond_0),
    .O(Mux2xBits2_inst0_O)
);
Mux2xBits2 Mux2xBits2_inst1 (
    .I0(a_mux_sel_4),
    .I1(a_mux_sel_3),
    .S(_cond_2),
    .O(Mux2xBits2_inst1_O)
);
Mux2xBits2 Mux2xBits2_inst2 (
    .I0(a_mux_sel_5),
    .I1(a_mux_sel_0),
    .S(_cond_3),
    .O(Mux2xBits2_inst2_O)
);
assign __0_return_0 = {Mux2xBit_inst5_O,Mux2xBits1_inst1_O[0],Mux2xBit_inst4_O,Mux2xBits2_inst2_O[1:0],Mux2xBit_inst7_O,Mux2xBit_inst6_O};
assign _cond_0 = do_swap_0;
assign _cond_2 = curr == 2'h1;
assign _cond_3 = curr == 2'h0;
assign a_mux_sel_0 = 2'h0;
assign a_mux_sel_1 = 2'h2;
assign a_mux_sel_2 = 2'h1;
assign a_mux_sel_3 = Mux2xBits2_inst0_O;
assign a_mux_sel_4 = 2'h0;
assign a_mux_sel_5 = Mux2xBits2_inst1_O;
assign a_reg_en_0 = 1'b1;
assign a_reg_en_1 = 1'b1;
assign a_reg_en_2 = 1'b0;
assign a_reg_en_3 = Mux2xBit_inst0_O;
assign b_mux_sel_0 = 1'h1;
assign b_mux_sel_1 = 1'h0;
assign b_mux_sel_2 = 1'h0;
assign b_mux_sel_3 = Mux2xBits1_inst0_O;
assign b_reg_en_0 = 1'b1;
assign b_reg_en_1 = do_swap_0;
assign b_reg_en_2 = 1'b0;
assign b_reg_en_3 = Mux2xBit_inst1_O;
assign do_swap_0 = is_a_lt_b;
assign magma_Bit_not_inst0_out = ~ is_b_zero;
assign magma_Bits_2_eq_inst2_out = curr == 2'h2;
assign req_rdy_0 = 1'b1;
assign req_rdy_1 = 1'b0;
assign req_rdy_2 = 1'b0;
assign req_rdy_3 = Mux2xBit_inst2_O;
assign resp_val_0 = 1'b0;
assign resp_val_1 = 1'b0;
assign resp_val_2 = 1'b1;
assign resp_val_3 = Mux2xBit_inst3_O;
assign O__0 = __0_return_0[0];
assign O__1 = __0_return_0[1];
assign O__2 = __0_return_0[3:2];
assign O__3 = __0_return_0[4];
assign O__4 = __0_return_0[5];
assign O__5 = __0_return_0[6];
endmodule

module Gcd16 (
    input clk,
    input [31:0] req_msg,
    output req_rdy,
    input req_val,
    input reset,
    output [15:0] resp_msg,
    input resp_rdy,
    output resp_val
);
wire [1:0] Mux2xBits2_inst0_O;
wire [1:0] Mux2xBits2_inst1_O;
wire [1:0] Mux2xBits2_inst2_O;
wire [1:0] Mux2xBits2_inst3_O;
wire [1:0] Mux2xBits2_inst4_O;
wire [1:0] Mux2xBits2_inst5_O;
wire [15:0] Mux2xUInt16_inst0_O;
wire [15:0] Mux3xUInt16_inst0_O;
wire [15:0] a_reg_O;
wire [15:0] b_reg_O;
wire [1:0] f3_inst0_O__2;
wire f3_inst0_O__3;
wire [0:0] f3_inst0_O__4;
wire f3_inst0_O__5;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bits_2_eq_inst0_out;
wire magma_Bits_2_eq_inst1_out;
wire magma_Bits_2_eq_inst2_out;
wire magma_UInt_16_eq_inst0_out;
wire [15:0] magma_UInt_16_sub_inst0_out;
wire magma_UInt_16_ult_inst0_out;
wire [1:0] next;
wire [1:0] state_O;
Mux2xBits2 Mux2xBits2_inst0 (
    .I0(state_O),
    .I1(2'h1),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xBits2_inst0_O)
);
Mux2xBits2 Mux2xBits2_inst1 (
    .I0(state_O),
    .I1(2'h2),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xBits2_inst1_O)
);
Mux2xBits2 Mux2xBits2_inst2 (
    .I0(state_O),
    .I1(2'h0),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xBits2_inst2_O)
);
Mux2xBits2 Mux2xBits2_inst3 (
    .I0(state_O),
    .I1(Mux2xBits2_inst2_O),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xBits2_inst3_O)
);
Mux2xBits2 Mux2xBits2_inst4 (
    .I0(Mux2xBits2_inst3_O),
    .I1(Mux2xBits2_inst1_O),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xBits2_inst4_O)
);
Mux2xBits2 Mux2xBits2_inst5 (
    .I0(Mux2xBits2_inst4_O),
    .I1(Mux2xBits2_inst0_O),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xBits2_inst5_O)
);
Mux2xUInt16 Mux2xUInt16_inst0 (
    .I0(a_reg_O),
    .I1(req_msg[31:16]),
    .S(f3_inst0_O__4[0]),
    .O(Mux2xUInt16_inst0_O)
);
Mux3xUInt16 Mux3xUInt16_inst0 (
    .I0(req_msg[15:0]),
    .I1(magma_UInt_16_sub_inst0_out),
    .I2(b_reg_O),
    .S(f3_inst0_O__2),
    .O(Mux3xUInt16_inst0_O)
);
Register a_reg (
    .I(Mux3xUInt16_inst0_O),
    .O(a_reg_O),
    .CE(f3_inst0_O__3),
    .CLK(clk)
);
Register b_reg (
    .I(Mux2xUInt16_inst0_O),
    .O(b_reg_O),
    .CE(f3_inst0_O__5),
    .CLK(clk)
);
f3 f3_inst0 (
    .O__0(req_rdy),
    .O__1(resp_val),
    .O__2(f3_inst0_O__2),
    .O__3(f3_inst0_O__3),
    .O__4(f3_inst0_O__4),
    .O__5(f3_inst0_O__5),
    .curr(state_O),
    .is_a_lt_b(magma_UInt_16_ult_inst0_out),
    .is_b_zero(magma_UInt_16_eq_inst0_out)
);
assign magma_Bit_and_inst0_out = req_val & req_rdy;
assign magma_Bit_and_inst1_out = (~ magma_UInt_16_ult_inst0_out) & magma_UInt_16_eq_inst0_out;
assign magma_Bit_and_inst2_out = resp_val & resp_rdy;
assign magma_Bits_2_eq_inst0_out = state_O == 2'h0;
assign magma_Bits_2_eq_inst1_out = state_O == 2'h1;
assign magma_Bits_2_eq_inst2_out = state_O == 2'h2;
assign magma_UInt_16_eq_inst0_out = b_reg_O == 16'h0000;
assign magma_UInt_16_sub_inst0_out = 16'(a_reg_O - b_reg_O);
assign magma_UInt_16_ult_inst0_out = a_reg_O < b_reg_O;
assign next = Mux2xBits2_inst5_O;
Register_unq1 state (
    .I(next),
    .O(state_O),
    .CLK(clk)
);
assign resp_msg = magma_UInt_16_sub_inst0_out;
endmodule


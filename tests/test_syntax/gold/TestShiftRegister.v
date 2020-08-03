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

module TestShiftRegister_comb (
    input [1:0] I,
    input [1:0] self_x_O,
    input [1:0] self_y_O,
    output [1:0] O0,
    output [1:0] O1,
    output [1:0] O2
);
assign O0 = I;
assign O1 = self_x_O;
assign O2 = self_y_O;
endmodule

module Register_comb (
    input [1:0] I,
    input [1:0] self_value_O,
    output [1:0] O0,
    output [1:0] O1
);
assign O0 = I;
assign O1 = self_value_O;
endmodule

module Register_unq1 (
    input [1:0] I,
    input CLK,
    output [1:0] O
);
wire [1:0] Register_comb_inst0_I;
wire [1:0] Register_comb_inst0_self_value_O;
wire [1:0] Register_comb_inst0_O0;
wire [1:0] Register_comb_inst0_O1;
wire reg_P_inst0_clk;
wire [1:0] reg_P_inst0_in;
wire [1:0] reg_P_inst0_out;
assign Register_comb_inst0_I = I;
assign Register_comb_inst0_self_value_O = reg_P_inst0_out;
Register_comb Register_comb_inst0 (
    .I(Register_comb_inst0_I),
    .self_value_O(Register_comb_inst0_self_value_O),
    .O0(Register_comb_inst0_O0),
    .O1(Register_comb_inst0_O1)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = Register_comb_inst0_O0;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h1),
    .width(2)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O = Register_comb_inst0_O1;
endmodule

module Register (
    input [1:0] I,
    input CLK,
    output [1:0] O
);
wire [1:0] Register_comb_inst0_I;
wire [1:0] Register_comb_inst0_self_value_O;
wire [1:0] Register_comb_inst0_O0;
wire [1:0] Register_comb_inst0_O1;
wire reg_P_inst0_clk;
wire [1:0] reg_P_inst0_in;
wire [1:0] reg_P_inst0_out;
assign Register_comb_inst0_I = I;
assign Register_comb_inst0_self_value_O = reg_P_inst0_out;
Register_comb Register_comb_inst0 (
    .I(Register_comb_inst0_I),
    .self_value_O(Register_comb_inst0_self_value_O),
    .O0(Register_comb_inst0_O0),
    .O1(Register_comb_inst0_O1)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = Register_comb_inst0_O0;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O = Register_comb_inst0_O1;
endmodule

module TestShiftRegister (
    input [1:0] I,
    input CLK,
    output [1:0] O
);
wire [1:0] Register_inst0_I;
wire Register_inst0_CLK;
wire [1:0] Register_inst0_O;
wire [1:0] Register_inst1_I;
wire Register_inst1_CLK;
wire [1:0] Register_inst1_O;
wire [1:0] TestShiftRegister_comb_inst0_I;
wire [1:0] TestShiftRegister_comb_inst0_self_x_O;
wire [1:0] TestShiftRegister_comb_inst0_self_y_O;
wire [1:0] TestShiftRegister_comb_inst0_O0;
wire [1:0] TestShiftRegister_comb_inst0_O1;
wire [1:0] TestShiftRegister_comb_inst0_O2;
assign Register_inst0_I = TestShiftRegister_comb_inst0_O0;
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .CLK(Register_inst0_CLK),
    .O(Register_inst0_O)
);
assign Register_inst1_I = TestShiftRegister_comb_inst0_O1;
assign Register_inst1_CLK = CLK;
Register_unq1 Register_inst1 (
    .I(Register_inst1_I),
    .CLK(Register_inst1_CLK),
    .O(Register_inst1_O)
);
assign TestShiftRegister_comb_inst0_I = I;
assign TestShiftRegister_comb_inst0_self_x_O = Register_inst0_O;
assign TestShiftRegister_comb_inst0_self_y_O = Register_inst1_O;
TestShiftRegister_comb TestShiftRegister_comb_inst0 (
    .I(TestShiftRegister_comb_inst0_I),
    .self_x_O(TestShiftRegister_comb_inst0_self_x_O),
    .self_y_O(TestShiftRegister_comb_inst0_self_y_O),
    .O0(TestShiftRegister_comb_inst0_O0),
    .O1(TestShiftRegister_comb_inst0_O1),
    .O2(TestShiftRegister_comb_inst0_O2)
);
assign O = TestShiftRegister_comb_inst0_O2;
endmodule


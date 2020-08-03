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

module TestBasic_comb (
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

module TestBasic (
    input [1:0] I,
    input CLK,
    output [1:0] O
);
wire [1:0] TestBasic_comb_inst0_I;
wire [1:0] TestBasic_comb_inst0_self_x_O;
wire [1:0] TestBasic_comb_inst0_self_y_O;
wire [1:0] TestBasic_comb_inst0_O0;
wire [1:0] TestBasic_comb_inst0_O1;
wire [1:0] TestBasic_comb_inst0_O2;
wire reg_P_inst0_clk;
wire [1:0] reg_P_inst0_in;
wire [1:0] reg_P_inst0_out;
wire reg_P_inst1_clk;
wire [1:0] reg_P_inst1_in;
wire [1:0] reg_P_inst1_out;
assign TestBasic_comb_inst0_I = I;
assign TestBasic_comb_inst0_self_x_O = reg_P_inst0_out;
assign TestBasic_comb_inst0_self_y_O = reg_P_inst1_out;
TestBasic_comb TestBasic_comb_inst0 (
    .I(TestBasic_comb_inst0_I),
    .self_x_O(TestBasic_comb_inst0_self_x_O),
    .self_y_O(TestBasic_comb_inst0_self_y_O),
    .O0(TestBasic_comb_inst0_O0),
    .O1(TestBasic_comb_inst0_O1),
    .O2(TestBasic_comb_inst0_O2)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = TestBasic_comb_inst0_O0;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign reg_P_inst1_clk = CLK;
assign reg_P_inst1_in = TestBasic_comb_inst0_O1;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_P_inst1 (
    .clk(reg_P_inst1_clk),
    .in(reg_P_inst1_in),
    .out(reg_P_inst1_out)
);
assign O = TestBasic_comb_inst0_O2;
endmodule


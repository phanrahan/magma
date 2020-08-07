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
    input [2:0] I,
    output [2:0] O,
    input CLK
);
wire reg_P_inst0_clk;
wire [2:0] reg_P_inst0_in;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(O)
);
endmodule

module Test2 (
    output [2:0] O,
    input CLK
);
wire [2:0] Register_inst0_I;
wire Register_inst0_CLK;
assign Register_inst0_I = 3'(O + 3'h1);
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(O),
    .CLK(Register_inst0_CLK)
);
endmodule


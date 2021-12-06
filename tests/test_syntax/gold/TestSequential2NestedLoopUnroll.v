module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

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

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module Register (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] Const_inst0_out;
wire [3:0] Const_inst1_out;
wire [3:0] reg_P4_inst0_out;
coreir_const #(
    .value(4'h0),
    .width(4)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_const #(
    .value(4'h0),
    .width(4)
) Const_inst1 (
    .out(Const_inst1_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P4_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P4_inst0_out)
);
coreir_term #(
    .width(4)
) term_inst0 (
    .in(Const_inst0_out)
);
coreir_term #(
    .width(4)
) term_inst1 (
    .in(Const_inst1_out)
);
assign O = reg_P4_inst0_out;
endmodule

module LoopUnroll (
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] Register_inst0_O;
wire [3:0] Register_inst1_O;
wire [3:0] Register_inst2_O;
wire [3:0] Register_inst3_O;
wire [3:0] Register_inst4_O;
wire [3:0] Register_inst5_O;
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
Register Register_inst2 (
    .I(Register_inst1_O),
    .O(Register_inst2_O),
    .CLK(CLK)
);
Register Register_inst3 (
    .I(Register_inst2_O),
    .O(Register_inst3_O),
    .CLK(CLK)
);
Register Register_inst4 (
    .I(Register_inst3_O),
    .O(Register_inst4_O),
    .CLK(CLK)
);
Register Register_inst5 (
    .I(Register_inst4_O),
    .O(Register_inst5_O),
    .CLK(CLK)
);
assign O = Register_inst5_O;
endmodule


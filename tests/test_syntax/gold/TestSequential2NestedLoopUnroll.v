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
    input [3:0] I,
    output [3:0] O,
    input CLK
);
wire [3:0] _reg_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) _reg (
    .clk(CLK),
    .in(I),
    .out(_reg_out)
);
assign O = _reg_out;
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
wire [3:0] call_result_O;
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
Register call_result (
    .I(Register_inst4_O),
    .O(call_result_O),
    .CLK(CLK)
);
assign O = call_result_O;
endmodule


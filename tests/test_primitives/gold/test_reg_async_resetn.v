module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module coreir_reg_arst #(
    parameter width = 1,
    parameter arst_posedge = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input arst,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg;
  wire real_rst;
  assign real_rst = arst_posedge ? arst : ~arst;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk, posedge real_rst) begin
    if (real_rst) outReg <= init;
    else outReg <= in;
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
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input ASYNCRESETN
);
wire [7:0] Const_inst0_out;
wire [7:0] reg_PRn8_inst0_out;
coreir_const #(
    .value(8'hde),
    .width(8)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b0),
    .clk_posedge(1'b1),
    .init(8'hde),
    .width(8)
) reg_PRn8_inst0 (
    .clk(CLK),
    .arst(ASYNCRESETN),
    .in(I),
    .out(reg_PRn8_inst0_out)
);
coreir_term #(
    .width(8)
) term_inst0 (
    .in(Const_inst0_out)
);
assign O = reg_PRn8_inst0_out;
endmodule

module test_reg_async_resetn (
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input ASYNCRESETN
);
wire [7:0] Const_inst0_out;
wire [7:0] Register_inst0_O;
coreir_const #(
    .value(8'hde),
    .width(8)
) Const_inst0 (
    .out(Const_inst0_out)
);
Register Register_inst0 (
    .I(I),
    .O(Register_inst0_O),
    .CLK(CLK),
    .ASYNCRESETN(ASYNCRESETN)
);
coreir_term #(
    .width(8)
) term_inst0 (
    .in(Const_inst0_out)
);
assign O = Register_inst0_O;
endmodule


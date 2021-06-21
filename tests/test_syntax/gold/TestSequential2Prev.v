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
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P3_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Test2 (
    output [2:0] O,
    input CLK
);
wire [2:0] magma_UInt_3_add_inst0_out;
Register Register_inst0 (
    .I(magma_UInt_3_add_inst0_out),
    .O(O),
    .CLK(CLK)
);
assign magma_UInt_3_add_inst0_out = 3'(O + 3'h1);
endmodule


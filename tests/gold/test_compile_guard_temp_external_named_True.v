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

module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module Register (
    input I,
    output O,
    input CLK
);
wire [0:0] reg_P1_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P1_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P1_inst0_out)
);
assign O = reg_P1_inst0_out[0];
endmodule

module DebugModule (
    input port_0,
    input CLK
);
wire reg_O;
Register reg (
    .I(port_0),
    .O(reg_O),
    .CLK(CLK)
);
endmodule

module Top (
    input I,
    output O,
    input CLK
);
wire temp_out;
`ifdef DEBUG
DebugModule DebugModule (
    .port_0(temp_out),
    .CLK(CLK)
);
`endif
corebit_wire temp (
    .in(I),
    .out(temp_out)
);
assign O = temp_out;
endmodule


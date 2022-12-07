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

module Mux2xArray3_Bits8 (
    input [7:0] I0 [2:0],
    input [7:0] I1 [2:0],
    input S,
    output [7:0] O [2:0]
);
reg [23:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = {I0[2],I0[1],I0[0]};
end else begin
    mux_out = {I1[2],I1[1],I1[0]};
end
end

assign O[2] = {mux_out[23],mux_out[22],mux_out[21],mux_out[20],mux_out[19],mux_out[18],mux_out[17],mux_out[16]};
assign O[1] = {mux_out[15],mux_out[14],mux_out[13],mux_out[12],mux_out[11],mux_out[10],mux_out[9],mux_out[8]};
assign O[0] = {mux_out[7],mux_out[6],mux_out[5],mux_out[4],mux_out[3],mux_out[2],mux_out[1],mux_out[0]};
endmodule

module Register (
    input [7:0] I [2:0],
    output [7:0] O [2:0],
    input CLK,
    input RESET
);
wire [7:0] Mux2xArray3_Bits8_inst0_O [2:0];
wire [23:0] _reg_out;
wire [7:0] Mux2xArray3_Bits8_inst0_I0 [2:0];
assign Mux2xArray3_Bits8_inst0_I0[2] = I[2];
assign Mux2xArray3_Bits8_inst0_I0[1] = I[1];
assign Mux2xArray3_Bits8_inst0_I0[0] = I[0];
wire [7:0] Mux2xArray3_Bits8_inst0_I1 [2:0];
assign Mux2xArray3_Bits8_inst0_I1[2] = 8'hbe;
assign Mux2xArray3_Bits8_inst0_I1[1] = 8'had;
assign Mux2xArray3_Bits8_inst0_I1[0] = 8'hde;
Mux2xArray3_Bits8 Mux2xArray3_Bits8_inst0 (
    .I0(Mux2xArray3_Bits8_inst0_I0),
    .I1(Mux2xArray3_Bits8_inst0_I1),
    .S(RESET),
    .O(Mux2xArray3_Bits8_inst0_O)
);
wire [23:0] _reg_in;
assign _reg_in = {Mux2xArray3_Bits8_inst0_O[2],Mux2xArray3_Bits8_inst0_O[1],Mux2xArray3_Bits8_inst0_O[0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'hbeadde),
    .width(24)
) _reg (
    .clk(CLK),
    .in(_reg_in),
    .out(_reg_out)
);
assign O[2] = {_reg_out[23],_reg_out[22],_reg_out[21],_reg_out[20],_reg_out[19],_reg_out[18],_reg_out[17],_reg_out[16]};
assign O[1] = {_reg_out[15],_reg_out[14],_reg_out[13],_reg_out[12],_reg_out[11],_reg_out[10],_reg_out[9],_reg_out[8]};
assign O[0] = {_reg_out[7],_reg_out[6],_reg_out[5],_reg_out[4],_reg_out[3],_reg_out[2],_reg_out[1],_reg_out[0]};
endmodule

module test_reg_of_nested_array (
    input [7:0] I [2:0],
    output [7:0] O [2:0],
    input CLK,
    input RESET
);
wire [7:0] Register_inst0_O [2:0];
wire [7:0] Register_inst0_I [2:0];
assign Register_inst0_I[2] = I[2];
assign Register_inst0_I[1] = I[1];
assign Register_inst0_I[0] = I[0];
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(CLK),
    .RESET(RESET)
);
assign O[2] = Register_inst0_O[2];
assign O[1] = Register_inst0_O[1];
assign O[0] = Register_inst0_O[0];
endmodule


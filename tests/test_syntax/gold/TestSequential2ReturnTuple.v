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
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P4_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Mux2x_SequentialRegisterWrapperBits4 (
    input [3:0] I0,
    input [3:0] I1,
    input S,
    output [3:0] O
);
reg [3:0] coreir_commonlib_mux2x4_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x4_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x4_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x4_inst0_out;
endmodule

module Mux2xBits4 (
    input [3:0] I0,
    input [3:0] I1,
    input S,
    output [3:0] O
);
reg [3:0] coreir_commonlib_mux2x4_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x4_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x4_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x4_inst0_out;
endmodule

module Basic (
    input [3:0] I,
    input S,
    output [3:0] O0,
    output [3:0] O1,
    input CLK
);
wire [3:0] Mux2xBits4_inst0_O;
wire [3:0] Mux2x_SequentialRegisterWrapperBits4_inst0_O;
wire [3:0] Register_inst0_O;
wire [3:0] Register_inst1_O;
Mux2xBits4 Mux2xBits4_inst0 (
    .I0(I),
    .I1(I),
    .S(S),
    .O(Mux2xBits4_inst0_O)
);
Mux2xBits4 Mux2xBits4_inst1 (
    .I0(I),
    .I1(Register_inst0_O),
    .S(S),
    .O(O1)
);
Mux2x_SequentialRegisterWrapperBits4 Mux2x_SequentialRegisterWrapperBits4_inst0 (
    .I0(Register_inst0_O),
    .I1(Register_inst0_O),
    .S(S),
    .O(Mux2x_SequentialRegisterWrapperBits4_inst0_O)
);
Mux2x_SequentialRegisterWrapperBits4 Mux2x_SequentialRegisterWrapperBits4_inst1 (
    .I0(Register_inst0_O),
    .I1(I),
    .S(S),
    .O(O0)
);
Register Register_inst0 (
    .I(Mux2xBits4_inst0_O),
    .O(Register_inst0_O),
    .CLK(CLK)
);
Register Register_inst1 (
    .I(Mux2x_SequentialRegisterWrapperBits4_inst0_O),
    .O(Register_inst1_O),
    .CLK(CLK)
);
endmodule

